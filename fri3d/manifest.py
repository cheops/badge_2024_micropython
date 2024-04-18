package("fri3d", base_path="./modules")

module("boot.py", base_path="./modules")
module("main.py", base_path="./modules")

module("fonts/bitmap/vga1_16x16.py", base_path="./s3lcd")

package("ota", base_path="./micropython-esp32-ota/mip")
package("semver", base_path="./modules")
package("toml", base_path="./modules")
package("wifi_manager", base_path="./modules")
