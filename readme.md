### Usage 

# 
    python3 AiortcBBB.py \
    --ws_url "wss://bbb.ostedhy.tn/bbb-webrtc-sfu?sessionToken=7cvithhhxjsm5vuv" \
    --sfu_component "screenshare" \
    --role "send" \
    --internalMeetingId "7c22338bce3c6e485ac2f2d872f2f24816d53011-1718092523886" \
    --userName "Amir" \
    --voice_bridge "66711" \
    --callerName "w_upakl74suq3s" \
    --cookies "_greenlight-3_0_session=eGX30V5NXtAH9LBHMXmKRosawsetd%2BOkVh4zwILG3m0RIoDc4eFovCeXknHeYdeq2WOKbeubD2HJDgI6ADrKFvXpinXdDHb%2FzZvUnRh%2FKCucyHORIjc61EKGYHt8yyF%2BGC8BFupYF%2FVDF5gSbjIXtb9KoQxP7MZL1O32OKMcr3XFe3%2FSOncbidmKEf%2F3FOSwBGX%2BAQHvvrt3F6qM8KUVHgTCLbJhQLGgnP2w1OsDuIHOy1Eeys5r0FiuDWRFZYg%2BhCxW7F%2BK9Gh69btG42GUW5pvh%2FxAzKGp6dabMb%2F4Tkkx%2FdGcdkRxuUpXPSXmofzHAYHie%2Bvm5Xs1FNt1F0H55D%2FiE4x0uOu4M%2FwwlsK5uK4SCSvZP8H755est6VDZRIQ8vDTY2a2mSVeNNQn4ExQmtpHFoj0f8zG09qwkQMa3x7cJf%2BF%2FB9wtuwoOw%3D%3D--O3OldhhhpjBzHlOv--iCE%2BLAyjm5TC7q0wT7BU%2Bw%3D%3D; JSESSIONID=BECC668454B5F2EBCD7D9E249274BBA9" \
    --turn_servers '[{"username": "1718178928:w_upakl74suq3s","password": "QXbTGY/LGtxSD+Abv8Bled//VFg=","url": "turns:bbb.ostedhy.tn:443?transport=tcp","ttl": 86400},{"username": "1718178928:w_upakl74suq3s","password": "QXbTGY/LGtxSD+Abv8Bled//VFg=","url": "turn:bbb.ostedhy.tn:3478","ttl": 86400}]'
o=- 3926879746 3926879746 IN IP4 0.0.0.0
s=-
t=0 0
a=group:BUNDLE 0
a=msid-semantic:WMS *
m=video 65043 UDP/TLS/RTP/SAVPF 97 98 99 100 101 102
c=IN IP4 192.168.1.20
a=sendrecv
a=extmap:1 urn:ietf:params:rtp-hdrext:sdes:mid
a=extmap:3 http://www.webrtc.org/experiments/rtp-hdrext/abs-send-time
a=mid:0
a=msid:14ce5ef8-2ad7-4dae-86af-d93e928361ee a30b65c6-963d-479e-a1c7-68195bad3263
a=rtcp:9 IN IP4 0.0.0.0
a=rtcp-mux
a=ssrc-group:FID 2036808779 681684451
a=ssrc:2036808779 cname:68f0d0a8-6e11-4f08-82d3-ad47bc5a43d8
a=ssrc:681684451 cname:68f0d0a8-6e11-4f08-82d3-ad47bc5a43d8
a=rtpmap:97 VP8/90000
a=rtcp-fb:97 nack
a=rtcp-fb:97 nack pli
a=rtcp-fb:97 goog-remb
a=rtpmap:98 rtx/90000
a=fmtp:98 apt=97
a=rtpmap:99 H264/90000
a=rtcp-fb:99 nack
a=rtcp-fb:99 nack pli
a=rtcp-fb:99 goog-remb
a=fmtp:99 level-asymmetry-allowed=1;packetization-mode=1;profile-level-id=42001f
a=rtpmap:100 rtx/90000
a=fmtp:100 apt=99
a=rtpmap:101 H264/90000
a=rtcp-fb:101 nack
a=rtcp-fb:101 nack pli
a=rtcp-fb:101 goog-remb
a=fmtp:101 level-asymmetry-allowed=1;packetization-mode=1;profile-level-id=42e01f
a=rtpmap:102 rtx/90000
a=fmtp:102 apt=101
a=candidate:40537ee97c0b7cd4fcd42ec8e27c5e50 1 udp 2130706431 192.168.1.20 65043 typ host
a=candidate:6ff94c704645a6638be76391a894c9c1 1 udp 16777215 37.187.38.168 54663 typ relay raddr 192.168.1.20 rport 53005
a=end-of-candidates
a=ice-ufrag:PySp
a=ice-pwd:GSNh8cWpt6VUexGJFXnnUQ
a=fingerprint:sha-256 2A:90:B4:7F:B9:78:B6:B7:76:06:7F:9C:41:A5:9C:EF:D8:59:97:0C:C6:53:BD:D5:0F:D4:82:7E:D9:E2:7D:8C
a=setup:actpass
--------
m=video 9 UDP/TLS/RTP/SAVPF 96 97 102 103 104 105 106 107 108 109 127 125 39 40 45 46 98 99 100 101 112 113 116 117 118
c=IN IP4 0.0.0.0
a=rtcp:9 IN IP4 0.0.0.0
a=ice-ufrag:+5eZ
a=ice-pwd:cxria1qsBptFVM12EhfWQYVw
a=ice-options:trickle
a=fingerprint:sha-256 EE:1B:3A:8D:1C:65:9F:60:A7:E8:3D:14:45:16:07:0C:49:49:D2:F7:B6:A3:E2:C3:FB:21:0A:FA:49:2A:B6:18
a=setup:actpass
a=mid:0
a=extmap:1 urn:ietf:params:rtp-hdrext:toffset
a=extmap:2 http://www.webrtc.org/experiments/rtp-hdrext/abs-send-time
a=extmap:3 urn:3gpp:video-orientation
a=extmap:4 http://www.ietf.org/id/draft-holmer-rmcat-transport-wide-cc-extensions-01
a=extmap:5 http://www.webrtc.org/experiments/rtp-hdrext/playout-delay
a=extmap:6 http://www.webrtc.org/experiments/rtp-hdrext/video-content-type
a=extmap:7 http://www.webrtc.org/experiments/rtp-hdrext/video-timing
a=extmap:8 http://www.webrtc.org/experiments/rtp-hdrext/color-space
a=extmap:9 urn:ietf:params:rtp-hdrext:sdes:mid
a=extmap:10 urn:ietf:params:rtp-hdrext:sdes:rtp-stream-id
a=extmap:11 urn:ietf:params:rtp-hdrext:sdes:repaired-rtp-stream-id
a=sendonly
a=msid:0702fe7d-720a-4c3a-a08f-c1017cb72fd0 7b930244-3486-4b5c-881a-2eccb211b295
a=rtcp-mux
a=rtcp-rsize
a=rtpmap:96 VP8/90000
a=rtcp-fb:96 goog-remb
a=rtcp-fb:96 transport-cc
a=rtcp-fb:96 ccm fir
a=rtcp-fb:96 nack
a=rtcp-fb:96 nack pli
a=rtpmap:97 rtx/90000
a=fmtp:97 apt=96
a=rtpmap:102 H264/90000
a=rtcp-fb:102 goog-remb
a=rtcp-fb:102 transport-cc
a=rtcp-fb:102 ccm fir
a=rtcp-fb:102 nack
a=rtcp-fb:102 nack pli
a=fmtp:102 level-asymmetry-allowed=1;packetization-mode=1;profile-level-id=42001f
a=rtpmap:103 rtx/90000
a=fmtp:103 apt=102
a=rtpmap:104 H264/90000
a=rtcp-fb:104 goog-remb
a=rtcp-fb:104 transport-cc
a=rtcp-fb:104 ccm fir
a=rtcp-fb:104 nack
a=rtcp-fb:104 nack pli
a=fmtp:104 level-asymmetry-allowed=1;packetization-mode=0;profile-level-id=42001f
a=rtpmap:105 rtx/90000
a=fmtp:105 apt=104
a=rtpmap:106 H264/90000
a=rtcp-fb:106 goog-remb
a=rtcp-fb:106 transport-cc
a=rtcp-fb:106 ccm fir
a=rtcp-fb:106 nack
a=rtcp-fb:106 nack pli
a=fmtp:106 level-asymmetry-allowed=1;packetization-mode=1;profile-level-id=42e01f
a=rtpmap:107 rtx/90000
a=fmtp:107 apt=106
a=rtpmap:108 H264/90000
a=rtcp-fb:108 goog-remb
a=rtcp-fb:108 transport-cc
a=rtcp-fb:108 ccm fir
a=rtcp-fb:108 nack
a=rtcp-fb:108 nack pli
a=fmtp:108 level-asymmetry-allowed=1;packetization-mode=0;profile-level-id=42e01f
a=rtpmap:109 rtx/90000
a=fmtp:109 apt=108
a=rtpmap:127 H264/90000
a=rtcp-fb:127 goog-remb
a=rtcp-fb:127 transport-cc
a=rtcp-fb:127 ccm fir
a=rtcp-fb:127 nack
a=rtcp-fb:127 nack pli
a=fmtp:127 level-asymmetry-allowed=1;packetization-mode=1;profile-level-id=4d001f
a=rtpmap:125 rtx/90000
a=fmtp:125 apt=127
a=rtpmap:39 H264/90000
a=rtcp-fb:39 goog-remb
a=rtcp-fb:39 transport-cc
a=rtcp-fb:39 ccm fir
a=rtcp-fb:39 nack
a=rtcp-fb:39 nack pli
a=fmtp:39 level-asymmetry-allowed=1;packetization-mode=0;profile-level-id=4d001f
a=rtpmap:40 rtx/90000
a=fmtp:40 apt=39
a=rtpmap:45 AV1/90000
a=rtcp-fb:45 goog-remb
a=rtcp-fb:45 transport-cc
a=rtcp-fb:45 ccm fir
a=rtcp-fb:45 nack
a=rtcp-fb:45 nack pli
a=fmtp:45 level-idx=5;profile=0;tier=0
a=rtpmap:46 rtx/90000
a=fmtp:46 apt=45
a=rtpmap:98 VP9/90000
a=rtcp-fb:98 goog-remb
a=rtcp-fb:98 transport-cc
a=rtcp-fb:98 ccm fir
a=rtcp-fb:98 nack
a=rtcp-fb:98 nack pli
a=fmtp:98 profile-id=0
a=rtpmap:99 rtx/90000
a=fmtp:99 apt=98
a=rtpmap:100 VP9/90000
a=rtcp-fb:100 goog-remb
a=rtcp-fb:100 transport-cc
a=rtcp-fb:100 ccm fir
a=rtcp-fb:100 nack
a=rtcp-fb:100 nack pli
a=fmtp:100 profile-id=1
a=rtpmap:101 rtx/90000
a=fmtp:101 apt=100
a=rtpmap:112 red/90000
a=rtpmap:113 rtx/90000
a=fmtp:113 apt=112
a=rtpmap:116 ulpfec/90000
a=ssrc-group:FID 2673839998 3226188635
a=ssrc:2673839998 cname:2K6ral3YXrSDIMh8
a=ssrc:2673839998 msid:0702fe7d-720a-4c3a-a08f-c1017cb72fd0 7b930244-3486-4b5c-881a-2eccb211b295
a=ssrc:3226188635 cname:2K6ral3YXrSDIMh8
a=ssrc:3226188635 msid:0702fe7d-720a-4c3a-a08f-c1017cb72fd0 7b930244-3486-4b5c-881a-2eccb211b295
