#!/bin/sh
# Manifest completeness + decode checks for every dataset category.
set -eu

root="$(cd "$(dirname "$0")/.." && pwd)"
dataset="$root/dataset"
failures=0

fail() {
    echo "FAIL: $1"
    failures=$((failures + 1))
}

decodes() {
    # Exit status only: warnings are expected in tracks/structure/degraded.
    ffmpeg -hide_banner -v error "$@" -f null - >/dev/null 2>&1
}

while IFS=, read -r file _; do
    [ "$file" = "file" ] && continue
    [ -f "$dataset/$file" ] || fail "missing manifest file: $file"
done < "$dataset/manifest.csv"

# normal/: must decode with zero errors.
for file in "$dataset"/normal/*; do
    out="$(ffmpeg -hide_banner -v error -i "$file" -f null - 2>&1)" || {
        fail "decode failed: ${file#"$dataset/"}"; continue; }
    [ -z "$out" ] || fail "decode errors: ${file#"$dataset/"}"
done

# Valid-but-tricky media: the decoder process must finish successfully.
for dir in degraded tracks structure mislabeled; do
    for file in "$dataset/$dir"/*; do
        decodes -i "$file" -map "0:v?" -map "0:a?" -fps_mode passthrough ||
            fail "decode process failed: ${file#"$dataset/"}"
    done
done

for file in "$dataset"/subtitles/*.avi "$dataset"/subtitles/*.mkv \
            "$dataset"/subtitles/*.vob "$dataset"/subtitles/*.ts; do
    decodes -i "$file" -map 0 -c:s copy || fail "decode process failed: ${file#"$dataset/"}"
done

check_sub() {
    ffmpeg -hide_banner -v error "$@" -c:s copy -f null - >/dev/null 2>&1
}
sub="$dataset/subtitles/subtitle_reference_mpeg4_mp3_720x480"
check_sub -sub_charenc GBK -i "$sub.gbk.srt" || fail "GBK SRT"
check_sub -sub_charenc BIG5 -i "$sub.big5.srt" || fail "Big5 SRT"
check_sub -i "$sub.utf8bom.srt" || fail "UTF-8 BOM SRT"
check_sub -i "$sub.utf16le.srt" || fail "UTF-16LE SRT"
check_sub -i "$sub.ssa" || fail "SSA"
check_sub -f microdvd -i "$sub.microdvd-25fps.sub" || fail "MicroDVD 25"
check_sub -f microdvd -i "$sub.microdvd-23.976fps-header.sub" || fail "MicroDVD 23.976"
check_sub -i "$sub.vobsub.idx" || fail "VobSub"

for dir in normal degraded damage tracks subtitles structure mislabeled; do
    echo "$dir: $(find "$dataset/$dir" -type f | wc -l | tr -d ' ')"
done
echo "failures: $failures"
[ "$failures" -eq 0 ]
