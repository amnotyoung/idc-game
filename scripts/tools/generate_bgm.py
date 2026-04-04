"""
Aid World — BGM 생성기
- bgm_office.wav     : 8비트 경쾌한 사무실 테마
- bgm_street.wav     : 따뜻하고 활기찬 피지 거리
- bgm_government.wav : 긴장감 있는 관청 분위기
"""
import numpy as np
from scipy.io import wavfile
import os

OUT = "/Users/nddn/Documents/Claude/Projects/IDC game/assets/music"
os.makedirs(OUT, exist_ok=True)

SAMPLE_RATE = 44100

def note_freq(note):
    names = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
    n = note[:-1]
    octave = int(note[-1])
    semitone = names.index(n) + (octave + 1) * 12
    return 440.0 * (2 ** ((semitone - 69) / 12))

def square_wave(freq, duration, volume=0.3, duty=0.5):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    return np.where((t * freq % 1) < duty, volume, -volume)

def triangle_wave(freq, duration, volume=0.2):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    return volume * (2 * np.abs(2 * (t * freq % 1) - 1) - 1)

def sine_wave(freq, duration, volume=0.2):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    return volume * np.sin(2 * np.pi * freq * t)

def noise_drum(duration, volume=0.15, decay=0.8):
    n = int(SAMPLE_RATE * duration)
    noise = np.random.uniform(-1, 1, n)
    env = np.exp(-np.linspace(0, decay * 20, n))
    return noise * env * volume

def envelope(wave, attack=0.005, release=0.02):
    n = len(wave)
    a, r = int(SAMPLE_RATE * attack), int(SAMPLE_RATE * release)
    env = np.ones(n)
    env[:a] = np.linspace(0, 1, a)
    env[-r:] = np.linspace(1, 0, r)
    return wave * env

def seq(notes_and_durations, wave_fn):
    segments = []
    for nd in notes_and_durations:
        if nd[0] == 'R':
            segments.append(np.zeros(int(SAMPLE_RATE * nd[1])))
        else:
            w = wave_fn(note_freq(nd[0]), nd[1])
            segments.append(envelope(w))
    return np.concatenate(segments)

def normalize_and_save(mix, filename, fade_dur=0.15):
    mix = mix / np.max(np.abs(mix)) * 0.85
    fade = int(SAMPLE_RATE * fade_dur)
    mix[-fade:] *= np.linspace(1, 0, fade)
    path = os.path.join(OUT, filename)
    wavfile.write(path, SAMPLE_RATE, mix.astype(np.float32))
    print(f"저장됨: {path}  ({len(mix)/SAMPLE_RATE:.1f}초)")


# ════════════════════════════════════════════════
# 1. bgm_office.wav — 8비트 경쾌한 사무실 테마
# ════════════════════════════════════════════════
def make_office():
    BPM = 148
    S = (60 / BPM) / 4   # 16분음표
    H = S * 2
    Q = S * 4

    melody_notes = [
        ('E5',H), ('G5',H), ('A5',Q), ('G5',H), ('E5',H),
        ('C5',H), ('D5',H), ('E5',Q), ('R',Q),
        ('E5',H), ('F5',H), ('G5',Q), ('A5',H), ('G5',H),
        ('D5',H), ('E5',H), ('C5',Q), ('R',Q),
        ('G5',H), ('A5',H), ('B5',Q), ('A5',H), ('G5',H),
        ('E5',H), ('F5',H), ('G5',Q), ('R',Q),
        ('A5',S), ('G5',S), ('A5',S), ('G5',S), ('E5',H), ('G5',H),
        ('C5',H), ('E5',H), ('G5',Q), ('R',Q),
        ('B5',S), ('A5',S), ('G5',S), ('F5',S), ('E5',H), ('C5',H),
        ('D5',S), ('E5',S), ('F5',S), ('G5',S), ('A5',Q), ('R',Q),
        ('G5',H), ('F5',H), ('E5',S), ('F5',S), ('G5',H),
        ('A5',H), ('G5',H), ('F5',Q), ('R',Q),
        ('E5',H), ('G5',H), ('A5',Q), ('G5',H), ('E5',H),
        ('C5',H), ('D5',H), ('E5',Q), ('R',Q),
        ('G5',S), ('A5',S), ('B5',S), ('A5',S), ('G5',H), ('E5',H),
        ('C5',H), ('E5',H), ('C5',Q), ('R',Q),
    ]
    counter_notes = [
        ('C5',Q), ('E5',Q), ('G5',Q), ('E5',Q),
        ('A4',Q), ('C5',Q), ('E5',Q), ('R',Q),
        ('C5',Q), ('E5',Q), ('G5',Q), ('A5',Q),
        ('B4',Q), ('D5',Q), ('G5',Q), ('R',Q),
        ('G4',Q), ('B4',Q), ('D5',Q), ('G5',Q),
        ('C5',Q), ('E5',Q), ('G5',Q), ('R',Q),
        ('A4',Q), ('C5',Q), ('E5',Q), ('G5',Q),
        ('G4',Q), ('B4',Q), ('E5',Q), ('R',Q),
        ('G4',Q), ('B4',Q), ('D5',Q), ('F5',Q),
        ('A4',Q), ('C5',Q), ('E5',Q), ('R',Q),
        ('G4',Q), ('A4',Q), ('B4',Q), ('D5',Q),
        ('E5',Q), ('G5',Q), ('A5',Q), ('R',Q),
        ('C5',Q), ('E5',Q), ('G5',Q), ('E5',Q),
        ('A4',Q), ('C5',Q), ('E5',Q), ('R',Q),
        ('G4',Q), ('B4',Q), ('D5',Q), ('G5',Q),
        ('C5',Q), ('E5',Q), ('C5',Q), ('R',Q),
    ]
    bass_notes = [
        ('C3',H), ('G3',H), ('C3',H), ('G3',H),
        ('A2',H), ('E3',H), ('A2',H), ('E3',H),
        ('C3',H), ('G3',H), ('C3',H), ('A3',H),
        ('G2',H), ('D3',H), ('G2',H), ('D3',H),
        ('G2',H), ('D3',H), ('G2',H), ('D3',H),
        ('C3',H), ('G3',H), ('C3',H), ('G3',H),
        ('A2',H), ('E3',H), ('A2',H), ('E3',H),
        ('C3',H), ('G3',H), ('C3',H), ('G3',H),
        ('G2',H), ('D3',H), ('G2',H), ('D3',H),
        ('A2',H), ('E3',H), ('A2',H), ('E3',H),
        ('G2',H), ('D3',H), ('G2',H), ('B2',H),
        ('E3',H), ('B2',H), ('E3',H), ('B2',H),
        ('C3',H), ('G3',H), ('C3',H), ('G3',H),
        ('A2',H), ('E3',H), ('A2',H), ('E3',H),
        ('G2',H), ('D3',H), ('G2',H), ('D3',H),
        ('C3',H), ('G3',H), ('C3',H), ('G3',H),
    ]

    def make_drums(bars=16):
        kick  = [1,0,0,0, 1,0,0,0, 1,0,0,0, 1,0,0,0]
        snare = [0,0,0,0, 1,0,0,0, 0,0,0,0, 1,0,0,0]
        hihat = [1,0,1,0, 1,0,1,0, 1,0,1,0, 1,0,1,0]
        segments = []
        for _ in range(bars):
            for i in range(16):
                chunk = np.zeros(int(SAMPLE_RATE * S))
                if kick[i]:  chunk += noise_drum(S, 0.25, 1.5)
                if snare[i]: chunk += noise_drum(S, 0.18, 0.6)
                if hihat[i]:
                    n = int(SAMPLE_RATE * S)
                    hh = np.random.uniform(-1,1,n) * 0.06
                    hh *= np.exp(-np.linspace(0, 8, n))
                    chunk += hh
                segments.append(chunk)
        return np.concatenate(segments)

    ch1   = seq(melody_notes,  lambda f,d: square_wave(f, d, 0.28, 0.5))
    ch2   = seq(counter_notes, lambda f,d: square_wave(f, d, 0.18, 0.25))
    ch3   = seq(bass_notes,    lambda f,d: triangle_wave(f, d, 0.22))
    drums = make_drums(16)
    n     = min(len(ch1), len(ch2), len(ch3), len(drums))
    mix   = ch1[:n] + ch2[:n] + ch3[:n] + drums[:n]
    normalize_and_save(mix, "bgm_office.wav")


# ════════════════════════════════════════════════
# 2. bgm_street.wav — 따뜻하고 활기찬 피지 거리
#    F장조, BPM=112, 경쾌한 스타카토 베이스 + 밝은 멜로디
# ════════════════════════════════════════════════
def make_street():
    BPM = 112
    S = (60 / BPM) / 4
    H = S * 2
    Q = S * 4
    DQ = Q * 1.5   # 점4분음표

    # 밝고 통통 튀는 멜로디 — F장조
    melody_notes = [
        ('F5',H),  ('A5',H),  ('C6',Q),  ('A5',H),  ('F5',H),
        ('G5',H),  ('A5',H),  ('G5',Q),  ('R',Q),
        ('A5',H),  ('C6',H),  ('D6',Q),  ('C6',H),  ('A5',H),
        ('G5',H),  ('F5',H),  ('C5',Q),  ('R',Q),

        ('C6',H),  ('D6',H),  ('C6',Q),  ('A5',H),  ('G5',H),
        ('F5',H),  ('G5',H),  ('A5',Q),  ('R',Q),
        ('F5',S),  ('G5',S),  ('A5',S),  ('G5',S),  ('F5',H),  ('C5',H),
        ('F5',Q),  ('R',DQ),

        # B 파트 — 약간 다른 전개
        ('D6',H),  ('C6',H),  ('A5',Q),  ('G5',H),  ('F5',H),
        ('E5',H),  ('F5',H),  ('G5',Q),  ('R',Q),
        ('A5',H),  ('G5',H),  ('F5',H),  ('E5',H),
        ('F5',Q),  ('C5',Q),  ('F5',Q),  ('R',Q),

        ('C6',H),  ('A5',H),  ('G5',Q),  ('F5',H),  ('G5',H),
        ('A5',H),  ('C6',H),  ('A5',Q),  ('R',Q),
        ('F5',S),  ('G5',S),  ('A5',S),  ('C6',S),  ('D6',H),  ('C6',H),
        ('F5',Q),  ('R',DQ),
    ]

    # 스타카토 베이스 (삼각파, 짧게 끊어서 팝하게)
    def stac_note(note_name, beats):
        dur_on  = beats * S * 0.55
        dur_off = beats * S * 0.45
        w = triangle_wave(note_freq(note_name), dur_on, 0.30)
        w = envelope(w, attack=0.006, release=0.04)
        return np.concatenate([w, np.zeros(int(SAMPLE_RATE * dur_off))])

    bass_seq = []
    # F-C-Dm-Bb 진행 × 4회
    progression = [
        [('F3',4),('C3',4),('A2',4),('C3',4)],  # F
        [('C3',4),('G2',4),('E3',4),('G2',4)],  # C
        [('D3',4),('A2',4),('F3',4),('A2',4)],  # Dm
        [('C3',4),('G2',4),('C3',4),('G2',4)],  # C
    ]
    for _ in range(4):
        for chord in progression:
            for note_name, beats in chord:
                bass_seq.append(stac_note(note_name, beats))
    bass = np.concatenate(bass_seq)

    # 하이햇 패턴 (16분음표)
    def make_hihat(total_steps):
        pattern = [1,0,1,1, 0,1,1,0, 1,0,1,1, 0,1,1,0]
        segments = []
        for i in range(total_steps):
            chunk_n = int(SAMPLE_RATE * S)
            if pattern[i % 16]:
                hh = np.random.uniform(-1,1,chunk_n) * 0.07
                hh *= np.exp(-np.linspace(0, 10, chunk_n))
                segments.append(hh)
            else:
                segments.append(np.zeros(chunk_n))
        return np.concatenate(segments)

    ch1 = seq(melody_notes, lambda f,d: square_wave(f, d, 0.26, 0.5))
    total_steps = len(melody_notes) * 0  # 멜로디 길이 기준으로 계산
    n_mel = len(ch1)
    # 멜로디 길이로 스텝 수 계산
    steps = int(np.ceil(n_mel / (SAMPLE_RATE * S)))
    hh = make_hihat(steps)

    n = min(len(ch1), len(bass), len(hh))
    mix = ch1[:n] + bass[:n] + hh[:n]
    normalize_and_save(mix, "bgm_street.wav")


# ════════════════════════════════════════════════
# 3. bgm_government.wav — 긴장감, 관료적 분위기
#    A단조, BPM=60, 느리고 무거운 드론 + 띄엄띄엄 멜로디
# ════════════════════════════════════════════════
def make_government():
    BPM = 60
    S = (60 / BPM) / 4
    H = S * 2
    Q = S * 4
    HN = Q * 2   # 2분음표
    WN = Q * 4   # 온음표

    # 뚝뚝 끊기는 단선율 멜로디 — A단조
    melody_notes = [
        ('A4', H),  ('R', H),
        ('G4', H),  ('F4', H),  ('R', Q),
        ('E4', H),  ('R', H),   ('R', Q),
        ('D4', Q),  ('E4', Q),  ('R', HN),

        ('A4', H),  ('R', Q),
        ('C5', H),  ('B4', H),  ('R', H),
        ('A4', HN), ('R', Q),
        ('G4', Q),  ('F4', Q),  ('R', HN),

        ('E5', H),  ('R', H),
        ('D5', H),  ('C5', H),  ('R', Q),
        ('B4', H),  ('A4', H),  ('R', Q),
        ('E4', HN), ('R', H),

        ('A4', Q),  ('G4', Q),  ('A4', H),  ('R', Q),
        ('F4', H),  ('E4', H),  ('R', H),
        ('D4', H),  ('E4', H),  ('R', Q),
        ('A3', WN),
    ]

    # 저음 드론 (A2 + E3 — 5도 음정, 긴장감)
    total_dur = sum(nd[1] for nd in melody_notes)
    drone_a = sine_wave(note_freq('A2'), total_dur, 0.14)
    drone_e = sine_wave(note_freq('E3'), total_dur, 0.09)
    # 가끔 울리는 낮은 종소리 느낌
    drone_a2 = sine_wave(note_freq('A3'), total_dur, 0.05)

    # 드론에 매우 느린 진폭 변조 (숨쉬는 느낌)
    n_drone = len(drone_a)
    lfo = 0.7 + 0.3 * np.sin(2 * np.pi * 0.1 * np.arange(n_drone) / SAMPLE_RATE)
    drone_a  *= lfo
    drone_e  *= lfo
    drone_a2 *= lfo

    # 랜덤 타이밍 낮은 피치 타격음 (불안감)
    def make_hits(total_n):
        out = np.zeros(total_n)
        hit_dur = int(SAMPLE_RATE * Q * 0.4)
        positions = [int(total_n * p) for p in [0.12, 0.31, 0.55, 0.74, 0.90]]
        for pos in positions:
            end = min(pos + hit_dur, total_n)
            hit = noise_drum(Q * 0.4, volume=0.18, decay=1.2)
            out[pos:end] += hit[:end-pos]
        return out

    ch1   = seq(melody_notes, lambda f,d: square_wave(f, d, 0.20, 0.5))
    n     = min(len(ch1), len(drone_a))
    hits  = make_hits(n)
    mix   = ch1[:n] + drone_a[:n] + drone_e[:n] + drone_a2[:n] + hits
    normalize_and_save(mix, "bgm_government.wav")


# ════════════════════════════════════════════════
# 4. bgm_island.wav — 나이탬바 섬 테마
#    C장조, BPM=72, 느리고 따뜻한 자연 느낌
#    사인파 멜로디 + 아르페지오 베이스
# ════════════════════════════════════════════════
def make_island():
    BPM = 72
    S = (60 / BPM) / 4   # 16분음표
    H = S * 2             # 8분음표
    Q = S * 4             # 4분음표
    DQ = Q * 1.5          # 점4분음표
    HN = Q * 2            # 2분음표
    WN = Q * 4            # 온음표

    # 사인파 부드러운 멜로디 — C장조, 느리고 단순
    melody_notes = [
        # A 파트 (8마디)
        ('E5', Q), ('G5', Q), ('A5', HN), ('R', Q),
        ('G5', Q), ('E5', Q), ('C5', HN), ('R', Q),
        ('D5', Q), ('F5', Q), ('G5', DQ), ('E5', Q), ('R', H),
        ('C5', HN), ('E5', Q), ('G5', Q), ('R', H),

        ('A5', Q), ('G5', Q), ('E5', HN), ('R', Q),
        ('F5', Q), ('E5', Q), ('D5', HN), ('R', Q),
        ('E5', Q), ('D5', Q), ('C5', DQ), ('R', Q), ('R', H),
        ('C5', WN),

        # B 파트 (8마디)
        ('G5', Q), ('A5', Q), ('G5', HN), ('R', Q),
        ('E5', Q), ('G5', Q), ('F5', HN), ('R', Q),
        ('D5', Q), ('E5', Q), ('F5', Q), ('G5', Q), ('A5', HN),
        ('G5', DQ), ('E5', Q), ('R', H),

        ('C6', Q), ('B5', Q), ('A5', HN), ('R', Q),
        ('G5', Q), ('A5', Q), ('G5', HN), ('R', Q),
        ('F5', Q), ('E5', Q), ('D5', DQ), ('C5', Q), ('R', H),
        ('C5', WN),
    ]

    # 아르페지오 베이스 — C장조 코드 진행 (Am-F-C-G)
    def arp_chord(notes, beat_dur, repeats=1):
        """코드 음표들을 아르페지오로 분해"""
        segments = []
        note_dur = beat_dur / len(notes)
        for _ in range(repeats):
            for n in notes:
                w = sine_wave(note_freq(n), note_dur, 0.18)
                w = envelope(w, attack=0.01, release=0.03)
                segments.append(w)
        return np.concatenate(segments)

    # C - Am - F - G 진행 × 4회 반복
    # 각 코드 = HN(2박) × 4코드 = 1마디(4박) 기준
    chord_prog = [
        (['C3', 'E3', 'G3'], HN),   # C
        (['A2', 'C3', 'E3'], HN),   # Am
        (['F2', 'A2', 'C3'], HN),   # F
        (['G2', 'B2', 'D3'], HN),   # G
    ]

    bass_segs = []
    for _ in range(16):   # 16마디 분량
        for chord_notes, dur in chord_prog:
            bass_segs.append(arp_chord(chord_notes, dur, 1))
    bass = np.concatenate(bass_segs)

    # 자연 느낌의 퍼커션 — 아주 부드러운 로우패스 드럼
    def make_soft_perc(total_n):
        out = np.zeros(total_n)
        step = int(SAMPLE_RATE * Q)
        # 약한 박자 클릭 (짝수 박)
        for i in range(0, total_n // step, 2):
            pos = i * step
            end = min(pos + int(SAMPLE_RATE * 0.06), total_n)
            click = np.random.uniform(-1, 1, end - pos)
            env = np.exp(-np.linspace(0, 12, end - pos))
            out[pos:end] += click * env * 0.06
        return out

    # 메인 멜로디 (사인파)
    ch1 = seq(melody_notes, lambda f, d: sine_wave(f, d, 0.25))

    # 부드러운 하모니 (멜로디 -3도 아래, 볼륨 낮게)
    harmony_notes = [
        ('C5', Q), ('E5', Q), ('F5', HN), ('R', Q),
        ('E5', Q), ('C5', Q), ('A4', HN), ('R', Q),
        ('B4', Q), ('D5', Q), ('E5', DQ), ('C5', Q), ('R', H),
        ('A4', HN), ('C5', Q), ('E5', Q), ('R', H),

        ('F5', Q), ('E5', Q), ('C5', HN), ('R', Q),
        ('D5', Q), ('C5', Q), ('B4', HN), ('R', Q),
        ('C5', Q), ('B4', Q), ('A4', DQ), ('R', Q), ('R', H),
        ('A4', WN),

        ('E5', Q), ('F5', Q), ('E5', HN), ('R', Q),
        ('C5', Q), ('E5', Q), ('D5', HN), ('R', Q),
        ('B4', Q), ('C5', Q), ('D5', Q), ('E5', Q), ('F5', HN),
        ('E5', DQ), ('C5', Q), ('R', H),

        ('A5', Q), ('G5', Q), ('F5', HN), ('R', Q),
        ('E5', Q), ('F5', Q), ('E5', HN), ('R', Q),
        ('D5', Q), ('C5', Q), ('B4', DQ), ('A4', Q), ('R', H),
        ('A4', WN),
    ]
    ch2 = seq(harmony_notes, lambda f, d: sine_wave(f, d, 0.12))

    n = min(len(ch1), len(ch2), len(bass))
    perc = make_soft_perc(n)
    mix = ch1[:n] + ch2[:n] + bass[:n] + perc[:n]
    normalize_and_save(mix, "bgm_island.wav")


# ── 실행 ──────────────────────────────────────────────────
print("=== BGM 생성 시작 ===")
print("1/4 사무실 테마...")
make_office()
print("2/4 거리 테마...")
make_street()
print("3/4 정부청사 테마...")
make_government()
print("4/4 섬 테마...")
make_island()
print("=== 완료! ===")
