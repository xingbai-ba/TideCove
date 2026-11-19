# Check optional tools (speech-to-text / text-to-speech)
#
# Both are optional: "installed is better, not installed still works".
#   - detected  -> report "enabled"; TideGleam.exe starts it in background itself
#   - missing   -> report "skipped"; nothing else is affected
#
# Called by the launcher .bat file. Keep all output ASCII so cmd never garbles it.

$ErrorActionPreference = 'SilentlyContinue'
$root = $PSScriptRoot
$appDir = Join-Path $root 'TideGleam'
$cfg = Join-Path $appDir 'config.json'

function Say($m) { Write-Host ("  " + $m) }

if (-not (Test-Path $cfg)) {
    Say 'Optional tools: no config.json yet, skipped (chat works fine without it).'
    exit 0
}

$c = $null
try { $c = Get-Content -Raw -Encoding UTF8 $cfg | ConvertFrom-Json } catch { $c = $null }
if (-not $c -or -not $c.tools) {
    Say 'Optional tools: config.json has no "tools" section, skipped.'
    exit 0
}

$py = [string]$c.tools.python
$hasPy = ($py -and (Test-Path $py))

# --- Speech to text (whisper) ---
$asrScript = Join-Path $appDir 'asr_server.py'
$modelDir = Join-Path $appDir 'models\whisper-small'
if (-not (Test-Path $asrScript)) {
    Say 'Speech-to-text: asr_server.py not found, skipped.'
} elseif (-not $hasPy) {
    Say 'Speech-to-text: Python not configured, skipped (only affects turning voice into text).'
} elseif (-not (Test-Path $modelDir) -and -not $env:ASR_MODEL) {
    Say 'Speech-to-text: model not found (TideGleam\models\whisper-small), skipped.'
} else {
    Say 'Speech-to-text: enabled (server will start it in background).'
}

# --- Text to speech (GPT-SoVITS) ---
$ttsScript = [string]$c.tools.ttsScript
$refAudio = [string]$c.tools.refAudio
if (-not $ttsScript) {
    Say 'Text-to-speech: ttsScript not configured, skipped (voice falls back to system TTS).'
} elseif (-not (Test-Path $ttsScript)) {
    Say 'Text-to-speech: ttsScript path does not exist, skipped.'
} elseif (-not $hasPy) {
    Say 'Text-to-speech: Python not configured, skipped.'
} elseif ($refAudio -and -not (Test-Path $refAudio)) {
    Say 'Text-to-speech: reference audio not found, skipped.'
} else {
    Say 'Text-to-speech: enabled (server will start it in background).'
}

exit 0