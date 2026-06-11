# FMT-Firmware BSP 适配信息清单

本文档汇总"为 FMT-Firmware 适配一块新飞控硬件平台"所需的信息,分两种典型场景:**全新 MCU + 全新板** 与 **MCU 同已有参考板(例如 s1) + 仅板级差异**。后者占工程中约 80% 的实际情况,工作量与风险显著低于前者。

适用对象:

- 计划在 FMT-Firmware 上新增 BSP 的工程师
- 评审新 BSP 引入工作量的项目经理
- 后续可能落地为 skill 的需求方(`fmt-bsp-derive-from-reference` / `fmt-bsp-bringup-author`)

## 1. 场景对照

| 场景 | 工作量 | 主要风险点 | 推荐路径 |
| --- | --- | --- | --- |
| 全新 MCU + 全新板 | 大 | 时钟方案、DMA 复用表、Cache 一致性、寄存器适配 | 完整 BSP bring-up |
| MCU 同参考板(s1 / mark2 等)+ 仅板级差异 | 小到中 | 引脚错配、传感器型号差异、电气量程偏差 | **从参考 BSP 派生差量适配** |
| MCU 同系列不同型号(例:F765 → F767) | 中 | 部分外设地址/中断号微调 | 派生 + 局部寄存器层校核 |

## 2. 场景 A:全新 BSP 适配 — 完整必需输入

按重要度排序;前 5 项缺一项就 block 大部分后续工作。

### 2.1 必需输入(缺一不可)

1. **MCU 精确型号 + 数据手册访问**
   - 例:`STM32H743VIH6` / `AT32F435ZMT7` / `MM32F5277E9P`(不是"STM32H7")
   - 至少能引用 RCC / GPIO / SPI / TIM / DMA / ADC 等关键章节
   - 内核类型、是否含 FPU / Cache、Word Length / Endianness

2. **完整引脚分配表**(来源:原理图)
   - 每个外设:`外设号 + 信号 + Port + Pin + AF`
   - 中断引脚(IMU INT / SBUS / Safety Switch 等)
   - GPIO 类(LED / 蜂鸣器)
   - ADC 通道与分压比

3. **时钟配置目标**
   - HSE 频率;是否含 LSE
   - 目标 SYSCLK / HCLK / APB1 / APB2
   - 低功耗模式需求

4. **外设上挂的具体器件型号**(寄存器集差异巨大,不能按"IMU 一概而论")
   - IMU:`ICM-42688P` / `BMI088` / `MPU9250` / `ICM-20689` / `ICM-20602`
   - 磁罗盘:`IST8310` / `RM3100` / `QMC5883L` / `HMC5883L`
   - 气压计:`BMP280` / `MS5611` / `SPL06-001` / `DPS310`
   - GPS 协议:`uBlox UBX` / `NMEA` / `DJI`
   - 接收机协议:`SBUS` / `CRSF` / `ELRS` / `PPM` / `DSM`
   - 电调协议:`PWM 400Hz` / `OneShot125` / `DShot300/600`

5. **软件栈选型**
   - 是否使用 FMT-Firmware I/O Device 框架
   - HAL 库版本与工具链(`arm-none-eabi-gcc 10.x` / `armcc` / `IAR` / `Keil`)
   - 构建系统(`SCons` / `CMake` / `MDK`)

### 2.2 强烈推荐输入

6. **相近板子的参考 BSP**:例如从 `STM32H750 BSP` 派生到 `STM32H743`
7. **中断与 DMA 分配偏好**:控制环 IMU 最高优先级;DMA 通道避免与 USB/SDIO 冲突
8. **启动方式与 Flash 分区**:bootloader / app / 参数 / 日志 / 备份
9. **RTOS 与节拍**:通常 RT-Thread + 1 kHz tick;控制环 400 Hz / 1 kHz

### 2.3 可选输入

- 板级 errata(芯片官方勘误)
- HIL 平台接口
- 已飞架次日志作 sanity check 基线
- 公司级编码规范

### 2.4 全新 BSP 最小起步包

提供这 4 项可立即产出 B 级输出:

1. MCU 精确型号
2. 完整引脚分配表
3. 至少 IMU + GPS + 接收机型号
4. 一个 FMT 现有 BSP 目录作为模板(例如 `bsp/stm32/stm32h750-fmt-mark2/`)

加上**寄存器手册关键章节文本** → 升至 A 级输出。

## 3. 场景 B:MCU 同参考板(s1 / mark2 等) — 差量适配

MCU 相同时 **80% 代码可从参考 BSP 复用** — HAL、启动、链接脚本、外设寄存器配置、中断向量表都不动。工作量集中在"**板级配线与外设器件型号差异**"。

### 3.1 必需输入

#### 3.1.1 引脚分配差异表(最重要)

只列出"参考板用什么 / 新板用什么"的差异项,不重发整张表。示例格式:

| 外设 | 信号 | 参考板 s1(PIN/AF) | 新板(PIN/AF) | 备注 |
| --- | --- | --- | --- | --- |
| SPI1 IMU | SCK | PA5/AF5 | PB3/AF5 | 改 |
| SPI1 IMU | CS | PC4(GPIO) | PA15(GPIO) | 改 |
| USART2 GPS | TX/RX | PD5/PD6 | PA2/PA3 | 改 |
| TIM5 PWM CH1 | — | PA0/AF2 | PA0/AF2 | 同 |
| LED1 | — | PE3 | PB14 | 改 |

> 每条改动只影响 `drv_<外设>.c` 中的引脚宏,不重写驱动核心逻辑。

#### 3.1.2 外设器件型号差异

| 类别 | 参考板 s1 | 新板 | 处置 |
| --- | --- | --- | --- |
| IMU | ICM-20689 | ICM-42688P | **驱动整换**(寄存器集不同) |
| 磁罗盘 | IST8310 | IST8310 | 复用 |
| 气压计 | MS5611 | SPL06-001 | **驱动整换** |
| GPS 模块 | M8N | F9P | 协议同(uBlox),仅配置参数 |
| 接收机 | SBUS | CRSF | **协议解析换**(UART 配置不同) |
| 电调 | PWM 400Hz | DShot300 | **PWM 输出层换**(Timer 配置差异大) |

#### 3.1.3 中断 / DMA 通道变化

仅在以下情况变化(因为 DMA 复用表由 MCU 决定,不会因板子变):

- 新板换了不同外设号(例:从 USART2 换到 UART4)
- 新板增加 / 减少了外设(例:多一路 CAN)

变化项给我即可,按芯片 DMA 复用表(MCU 同 → 不变)重排。

### 3.2 强烈推荐输入

4. **晶振频率是否一致**
   - 若同(常见 s1 = 25 MHz HSE,新板亦同):时钟配置完全复用
   - 若变:仅改 `system_clock.c` 中 PLL 配置

5. **电气量程差异**
   - 电池电压分压比(s1 为 `11:1` → 新板可能为 `21:1`)
   - 电流传感器 `xx mV/A`
   - ADC `VREF+` 参考电压
   - → 改 `drv_adc.c` 换算系数 + 参数表默认值

6. **传感器安装方向(`board_to_body` 旋转矩阵)**
   - IMU 在新板上的安装朝向(轴系是否需重映射)
   - 磁罗盘安装位置(内置 vs 外置)
   - → 改 `param/sensor_param.c` 默认值

7. **PWM 通道与电机编号约定**
   - `MOTOR1` 对应哪个 TIM 通道 / 旋转方向
   - 多旋翼编号约定(BetaFlight / PX4 / FMT 序列)
   - → 改 `actuator_map.c`

8. **LED / 蜂鸣器 / Safety Switch 极性**
   - 高 / 低电平点亮
   - PWM 蜂鸣器 vs 普通 GPIO
   - → 改 `drv_led.c` / `drv_buzzer.c`

### 3.3 可选输入

- SD 卡 / 外置 Flash 接法(若与 s1 不同)
- USB 接法
- CAN / Ethernet(若新增)
- 机壳约束(外置磁罗盘 / 外置气压计)

### 3.4 不需要重新提供的(MCU 相同时可全量复用)

- MCU 数据手册 / 参考手册
- HAL 库版本与启动代码(`startup_stm32xxx.s`)
- 链接脚本(若 Flash / RAM 大小一致)
- 大部分外设驱动**核心逻辑**(SPI / UART / I2C / Timer 寄存器配置完全相同)
- 设备模型框架接入方式
- `mcn` topic 命名约定
- `mlog` 框架接入
- 参数表 / 任务表 结构

### 3.5 MCU-同 场景的最小起步包

只需要这 3 项,可立即产出**完整可编译的新板 BSP**(从参考板派生):

1. **引脚差异表**(只列变化项)
2. **传感器型号差异表**(IMU / 磁罗盘 / 气压计 / 接收机 / 电调 协议层)
3. **电气量程差异**(电池分压比 / 电流系数;若与参考板完全一致可省)

再加一句"晶振频率与参考板是否一致" → 起步包齐。

## 4. 交付等级(无论场景 A / B 均适用)

| 等级 | 内容 | 前提 |
| --- | --- | --- |
| **A. 可直接编译运行的代码** | 完整 `bsp/<board>/`:`board.c/h`、`drv_*`、传感器驱动骨架、设备模型注册、链接脚本、`SConscript` | 必需输入全部 + 参考 BSP 齐 |
| **B. 框架完整 + 关键寄存器配置** | 同 A,但某些细节(具体寄存器位 / DMA stream 编号)留 `TODO` 让工程师按手册填 | 必需输入齐,但参考 BSP 缺失 |
| **C. 框架与接口骨架** | 文件结构 + 函数原型 + 注释里写清要按手册填什么 | 仅引脚表 + MCU 型号,无寄存器手册 |
| **D. 方案文档** | 仅"该怎么做"的步骤说明,不写代码 | 输入严重不足,继续写代码风险高 |

**场景 B(MCU 同参考板)通常可达 A 级**,因为参考 BSP 直接提供了所有寄存器层与框架代码;只需在其基础上做 patch / diff。

**场景 A(全新)默认从 B 级起步**,根据数据手册章节贴入情况升至 A 级。

## 5. 无法替代的硬件验证项

无论哪一级输出,以下必须由真实硬件验证,**Claude 无法保证**:

1. **时序边界** — SPI 时钟相位、I2C 上升沿、DMA + Cache 一致性
2. **板级电气问题** — 上拉 / 下拉、电平不匹配、信号完整性
3. **vendor 勘误** — 芯片 errata 可能未在我的知识里
4. **首次 bring-up** — 必须有逻辑分析仪 / 示波器 / J-Link
5. **IMU 校准与轴系定义** — `board_to_body` 旋转矩阵需实测验证
6. **电调标定与 PWM 极性** — 必须空载测试
7. **电压采样精度** — 实测分压比偏差

## 6. 后续可沉淀的 skill 候选

以下 skill 可基于本文档形成,落到 `fmt/` 库:

| Skill 名(建议) | 职责 | 主要工件 |
| --- | --- | --- |
| `fmt-bsp-derive-from-reference` | 从参考板派生新板 BSP — 基于差量输入产出 patch / 完整目录 | `bsp_derive_plan` |
| `fmt-bsp-bringup-author` | 全新 BSP bring-up 计划 — 完整必需输入下产出 BSP 骨架与 bring-up 检查清单 | `bsp_bringup_skeleton` |
| `fmt-bsp-pinmap-validator` | 校验引脚分配表与 MCU 复用能力的一致性 | `pinmap_validation_report` |
| `fmt-sensor-driver-author` | 单传感器驱动作者(指定型号 + 总线 + 工作模式) | `sensor_driver_skeleton` |

每个 skill 落地前对照 `fmt/_meta/first-principles-skill-contract.md` 与 `fmt/_meta/repo-management.md` 规范。

## 7. 快速决策树

新 BSP 需求来时,按下面顺序判定:

```
是否 MCU 与现有 FMT BSP 完全相同?
├─ 是 → 场景 B(差量适配)
│       ├─ 提供"§3.5 最小起步包"3 项
│       └─ 期望 A 级输出
└─ 否 ─┐
       是否 MCU 在同系列?(例:F765 ↔ F767)
       ├─ 是 → 场景 A.2(派生 + 局部校核)
       │       提供 §2.4 + 同系列差异(地址 / 中断号)
       └─ 否 → 场景 A(全新)
               提供 §2.4 最小起步包,期望 B 级起步
```

## 8. 维护说明

- 本文档随 FMT BSP 实际适配经验持续修订
- 新增 BSP 后,请把"实际遇到的坑"补回本文档第 5 节
- 新增 skill 时,在第 6 节登记
- 与 `control-law-mbd/` 库的接口契约相关时(`bridge_layer_contract` / `firmware_context`),交叉引用 `control-law-mbd/_meta/artifact-handoff-contract.md`
