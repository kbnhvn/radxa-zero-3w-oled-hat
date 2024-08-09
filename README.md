# radxa-zero-3w-oled-hate
Conf and overlay to use waveshare 1.3 oled hat with radxa zero 3w

Overlay .dts add pull-ups for buttons and joystick pins.

## GPIO Configuration

| Button      | BCM  | PIN | RADXA      | bank:pin |
|-------------|------|-----|------------|----------|
| key1        | p21  | 40  | GPIO3_A5   | 3:5      |
| key2        | P20  | 38  | GPIO3_A6   | 3:6      |
| key3        | p16  | 36  | GPIO3_A7   | 3:7      |
| Joy-up      | p6   | 31  | GPIO3_B4   | 3:12     |
| Joy-down    | p19  | 35  | GPIO3_A4   | 3:4      |
| Joy-left    | p5   | 29  | GPIO3_B3   | 3:11     |
| Joy-right   | p26  | 37  | GPIO1_A4   | 1:4      |
| Joy-press   | p13  | 33  | GPIO3_C3   | 3:19     |

## SPI Configuration

| Function   | PIN | RADXA        | bank:pin |
|------------|-----|--------------|----------|
| RST_PIN    | 22  | GPIO3_C1     | 3:17     |
| DC_PIN     | 18  | GPIO3_B2     | 3:10     |
| CS_PIN     | 24  | SPI3_CS0_M1  | 4:22     |

USE SPIDEV3.0
