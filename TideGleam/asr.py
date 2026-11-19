# -*- coding: utf-8 -*-
"""把一段音频转成文字（本地 whisper-small，GPU 优先）

用法：
    python asr.py <音频文件>

输出：{"text": "..."} 或 {"error": "..."}
"""
import sys
import json
import os
import traceback

_HERE = os.path.dirname(os.path.abspath(__file__))


def _find_model():
    """模型目录：环境变量 > 包内 models\whisper-small > 本机默认路径"""
    p = os.environ.get('ASR_MODEL')
    if p and os.path.isdir(p):
        return p
    for rel in ('models/whisper-small', os.path.join('models', 'whisper-small')):
        cand = os.path.join(_HERE, rel)
        if os.path.isdir(cand):
            return cand
    return r'E:\肥鱼\checkpoints\hf_cache\models--openai--whisper-small\snapshots\973afd24965f72e36ca33b3055d56a652f456b4d'


MODEL_DIR = _find_model()

_state = {'model': None, 'proc': None, 'device': 'cpu'}


def load():
    if _state['model'] is not None:
        return
    import torch
    from transformers import WhisperProcessor, WhisperForConditionalGeneration
    dev = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = WhisperForConditionalGeneration.from_pretrained(MODEL_DIR)
    proc = WhisperProcessor.from_pretrained(MODEL_DIR)
    # 旧接口：用 processor 生成「中文 + 转写」的强制解码提示，避开新 API 的 language 参数
    try:
        forced = proc.get_decoder_prompt_ids(language='zh', task='transcribe')
        model.generation_config.forced_decoder_ids = forced
    except Exception:
        model.generation_config.forced_decoder_ids = None
    model.generation_config.language = None
    model.generation_config.task = None
    model.to(dev)
    _state.update(model=model, proc=proc, device=dev)


def to_simplified(text):
    try:
        from opencc import OpenCC
        global _cc
        if _cc is None:
            _cc = OpenCC('t2s')
        return _cc.convert(text)
    except Exception:
        return text


_cc = None


def load_audio(path):
    """读成 16k 单声道 float32。librosa 解不了的格式（m4a/aac）用 PyAV 兜底。"""
    try:
        import librosa
        audio, sr = librosa.load(path, sr=16000, mono=True)
        if audio.size:
            return audio, sr
    except Exception:
        pass

    # PyAV 自带解码器，不依赖系统装 ffmpeg
    import av
    import numpy as np
    container = av.open(path)
    try:
        stream = next(s for s in container.streams if s.type == 'audio')
        resampler = av.audio.resampler.AudioResampler(format='s16', layout='mono', rate=16000)
        chunks = []
        for frame in container.decode(stream):
            for f in resampler.resample(frame):
                a = f.to_ndarray().reshape(-1)
                if a.size:
                    chunks.append(a)
        try:
            for f in resampler.resample(None):
                a = f.to_ndarray().reshape(-1)
                if a.size:
                    chunks.append(a)
        except Exception:
            pass
    finally:
        try:
            container.close()
        except Exception:
            pass

    if not chunks:
        raise RuntimeError('解不出音频数据（格式不支持？）')
    pcm = np.concatenate(chunks).astype('float32') / 32768.0
    return pcm, 16000


def transcribe(path):
    load()
    import numpy as np
    audio, sr = load_audio(path)
    if audio.size < 800:  # 不到 0.05 秒，当没声音
        return ''
    feats = _state['proc'](audio, sampling_rate=sr, return_tensors='pt').input_features
    feats = feats.to(_state['device'])
    with _no_grad():
        ids = _state['model'].generate(feats)
    raw = _state['proc'].batch_decode(ids, skip_special_tokens=True)[0].strip()
    return to_simplified(raw)


class _no_grad:
    def __enter__(self):
        import torch
        self._ctx = torch.no_grad()
        return self._ctx.__enter__()

    def __exit__(self, *a):
        return self._ctx.__exit__(*a)


if __name__ == '__main__':
    try:
        if len(sys.argv) < 2:
            print(json.dumps({'error': '用法: python asr.py <音频文件>'}, ensure_ascii=False))
            sys.exit(2)
        print(json.dumps({'text': transcribe(sys.argv[1])}, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({'error': str(e), 'trace': traceback.format_exc()[-600:]}, ensure_ascii=False))
        sys.exit(1)
