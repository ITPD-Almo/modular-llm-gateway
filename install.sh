#!/bin/sh
# Install an isolated gateway toolchain without sudo, Git, or system Python.
set -eu

main() {
    ref=main
    run_demo=1
    while [ "$#" -gt 0 ]; do
        case "$1" in
            --ref) [ "$#" -ge 2 ] || die '--ref needs a commit, tag or branch'; ref=$2; shift 2 ;;
            --no-demo) run_demo=0; shift ;;
            --help) printf '%s\n' 'Usage: sh install.sh [--ref COMMIT_OR_TAG] [--no-demo]'; return 0 ;;
            *) die "Unknown argument: $1" ;;
        esac
    done
    case "$ref" in ''|*[!a-zA-Z0-9._-]*) die 'Ref must contain only letters, digits, dot, underscore or hyphen' ;; esac
    case "$(uname -s):$(uname -m)" in
        Linux:x86_64|Linux:aarch64|Linux:arm64|Darwin:x86_64|Darwin:arm64) ;;
        *) die 'This installer targets Linux and macOS on x86_64/ARM64. See docs/terminal.md for requirements.' ;;
    esac
    : "${HOME:?HOME must name a writable user directory}"
    root=${XDG_DATA_HOME:-"$HOME/.local/share"}/llmgw
    bindir=${GATEWAY_BIN_DIR:-"$HOME/.local/bin"}
    case "$root:$bindir" in *"'"*|*'
'*) die 'Installation paths cannot contain a single quote or newline' ;; esac
    case "$root" in /*) ;; *) die 'XDG_DATA_HOME must be an absolute path' ;; esac
    case "$bindir" in /*) ;; *) die 'GATEWAY_BIN_DIR must be an absolute path' ;; esac
    command -v tar >/dev/null 2>&1 || die 'tar is required'
    mkdir -p "$root" "$bindir"
    # Never replace an unrelated executable or a shell profile.
    marker='# llmgw-managed-launcher'
    if [ -e "$bindir/llmgw" ] || [ -L "$bindir/llmgw" ]; then
        if [ -L "$bindir/llmgw" ] || ! grep -Fq "$marker" "$bindir/llmgw"; then
            die "Refusing to replace $bindir/llmgw; choose GATEWAY_BIN_DIR"
        fi
    fi
    scratch=$(mktemp -d "${TMPDIR:-/tmp}/llmgw-install.XXXXXXXX")
    trap 'rm -rf "$scratch"' EXIT
    trap 'exit 130' INT
    trap 'exit 143' TERM
    printf '%s\n' "Installing Modular LLM Gateway ($ref) for $(uname -s)/$(uname -m)"
    # Download the complete installer before executing it. uv stays private to
    # llmgw and never replaces a user's existing uv or system Python.
    download 'https://astral.sh/uv/0.11.31/install.sh' "$scratch/uv-install.sh"
    UV_INSTALL_DIR="$root/uv" UV_NO_MODIFY_PATH=1 sh "$scratch/uv-install.sh"
    download "https://github.com/ITPD-Almo/modular-llm-gateway/archive/$ref.tar.gz" "$scratch/source.tar.gz"
    mkdir "$scratch/source"
    tar -xzf "$scratch/source.tar.gz" -C "$scratch/source" --strip-components=1
    [ -f "$scratch/source/requirements-runtime.txt" ] || die 'This ref predates the terminal installer; choose the terminal preview or a newer release'
    UV_TOOL_DIR="$root/tools" UV_TOOL_BIN_DIR="$root/bin" UV_PYTHON_INSTALL_DIR="$root/python" \
        "$root/uv/uv" tool install --no-config --managed-python --python 3.12.13 \
        --reinstall --constraint "$scratch/source/requirements-runtime.txt" \
        "$scratch/source"
    launcher=$(mktemp "$bindir/.llmgw.XXXXXXXX")
    printf '%s\n' '#!/bin/sh' "$marker" "exec '$root/bin/llmgw' \"\$@\"" > "$launcher"
    chmod 755 "$launcher"
    mv -f "$launcher" "$bindir/llmgw"
    printf '%s\n' "Source ref: $ref" > "$root/install-receipt.txt"
    "$bindir/llmgw" doctor
    if [ "$run_demo" -eq 1 ]; then "$bindir/llmgw" demo; fi
    printf '\n%s\n' "Installed: $bindir/llmgw" 'Start the local server: llmgw serve'
    case ":$PATH:" in *":$bindir:"*) ;; *)
        printf '%s\n' "For this shell: export PATH=\"$bindir:\$PATH\"" "Or run directly: '$bindir/llmgw' serve"
    esac
    printf '%s\n' 'No shell profile was edited. No provider key or account is needed for the fake-provider demo.'
}

die() { printf 'llmgw installer: %s\n' "$*" >&2; exit 1; }

download() {
    if command -v curl >/dev/null 2>&1; then
        curl --proto '=https' --tlsv1.2 --fail --location --silent --show-error \
            --retry 2 --connect-timeout 20 --max-time 300 "$1" -o "$2"
    elif command -v wget >/dev/null 2>&1; then
        wget --https-only --timeout=30 --tries=3 -q "$1" -O "$2"
    else
        die 'curl or wget is required to download the isolated runtime'
    fi
}

main "$@"
