# Raw input and output
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

# this one is raw speaker but can change mic level

# 1. The Default Hijack (Must be at the top to claim Index 1)
pcm.!default {
    type asym
    playback.pcm "speaker_raw"
    capture.pcm "mic_plug"
}

# 2. Speaker Output (Raw hardware for max volume + Mono/Stereo fix)
pcm.speaker_raw {
    type plug
    slave.pcm "hw:0,0"
}

# 3. Mic Input (Mono/Stereo fix)
pcm.mic_plug {
    type plug
    slave.pcm "mic_boost"
}

# 4. Mic Volume Booster
pcm.mic_boost {
    type softvol
    slave.pcm "hw:0,0"
    control {
        name "Mic Capture Volume"
        card 0
    }
    min_dB -10.0
    max_dB 20.0
}

# OR old one i found in chat history:

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