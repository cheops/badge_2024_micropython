include("$(PORT_DIR)/boards/FRI3D_BADGE_COMMON/manifest.py")

package("fri3d", base_path="./modules")

module("wsen_isds.py", base_path="$(MPY_DIR)/fri3d/driver/WSEN_ISDS")
