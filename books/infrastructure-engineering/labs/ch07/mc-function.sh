mc() {
  docker run --rm --network cloudlab -v "$PWD":/work -w /work \
    -e MC_HOST_local=http://admin:change-me-please@minio:9000 \
    cgr.dev/chainguard/minio-client "$@"
}
