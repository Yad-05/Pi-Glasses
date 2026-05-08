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


OR old one i found in chat history:

pcm.!default {
  type asym
  capture.pcm "mic"
  playback.pcm "speaker"
}

# --- MICROPHONE SETTINGS ---
pcm.mic_sv {
  type softvol
  slave.pcm "hw:0,0"
  control {
    name "Boost Capture Volume"
    card 0
  }
  min_dB -5.0
  max_dB 30.0
}

pcm.mic {
  type plug
  slave.pcm "mic_sv"
}

# --- SPEAKER SETTINGS ---
pcm.speaker_sv {
  type softvol
  slave.pcm "hw:0,0"
  control {
    name "Speaker Playback Volume"
    card 0
  }
  min_dB -40.0
  max_dB 0.0
}

pcm.speaker {
  type plug
  slave.pcm "speaker_sv"
}