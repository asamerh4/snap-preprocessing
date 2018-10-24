set -e

BUILD=$(git rev-parse --short HEAD)

YELLOW='\033[1;33m'
NC='\033[0m' # No Color

docker build -t asamerh4/snap-preprocessing:$BUILD .

echo -e ${YELLOW}"**build finished -> asamerh4/snap-preprocessing:$BUILD"${NC}
