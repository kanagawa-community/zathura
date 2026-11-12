# Window hook for .github/scripts/capture-windows.sh: zathura opens a fixed page with
# each theme, recolored, with a search for "Kanagawa", so the page, the matches
# and the status bar show.
# Requires: zathura with a PDF plugin, rsvg-convert.
# shellcheck shell=bash
name=zathura
x11=yes
size=900x620

setup() {
  rsvg-convert -f pdf -o "$work/home/the-great-wave.pdf" "$root/scripts/fixtures/page.svg"
}

launch() {
  mkdir -p "$work/zathura-$1"
  cp "$root/themes/kanagawa-$1" "$work/zathura-$1/zathurarc"
  printf 'set window-width 900\nset window-height 620\nset adjust-open best-fit\nset recolor true\nset statusbar-home-tilde true\n' \
    >>"$work/zathura-$1/zathurarc"
  printf 'env HOME=%s GDK_BACKEND=x11 GSK_RENDERER=cairo zathura --config-dir=%s --data-dir=%s --find=Kanagawa %s' \
    "$work/home" "$work/zathura-$1" "$work/zathura-data" "$work/home/the-great-wave.pdf"
}
