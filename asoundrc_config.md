pcm.!default {
    type asym
    playback.pcm "speaker"
    capture.pcm "mic"
}

pcm.speaker {
    type plug
    slave.pcm "hw:0,0"
}

pcm.mic {
    type plug
    slave.pcm "hw:0,0"
}