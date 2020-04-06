/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.h
  * @brief          : Header for main.c file.
  *                   This file contains the common defines of the application.
  ******************************************************************************
  * @attention
  *
  * <h2><center>&copy; Copyright (c) 2020 STMicroelectronics.
  * All rights reserved.</center></h2>
  *
  * This software component is licensed by ST under Ultimate Liberty license
  * SLA0044, the "License"; You may not use this file except in compliance with
  * the License. You may obtain a copy of the License at:
  *                             www.st.com/SLA0044
  *
  ******************************************************************************
  */
/* USER CODE END Header */

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __MAIN_H
#define __MAIN_H

#ifdef __cplusplus
extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include "stm32f1xx_hal.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

/* Exported types ------------------------------------------------------------*/
/* USER CODE BEGIN ET */

/* USER CODE END ET */

/* Exported constants --------------------------------------------------------*/
/* USER CODE BEGIN EC */

/* USER CODE END EC */

/* Exported macro ------------------------------------------------------------*/
/* USER CODE BEGIN EM */

/* USER CODE END EM */

/* Exported functions prototypes ---------------------------------------------*/
void Error_Handler(void);

/* USER CODE BEGIN EFP */

/* USER CODE END EFP */

/* Private defines -----------------------------------------------------------*/
#define USB_INT_Pin GPIO_PIN_0
#define USB_INT_GPIO_Port GPIOA
#define LED_Pin GPIO_PIN_1
#define LED_GPIO_Port GPIOA
#define USB_PULLUP_Pin GPIO_PIN_3
#define USB_PULLUP_GPIO_Port GPIOA
#define NSS_Pin GPIO_PIN_4
#define NSS_GPIO_Port GPIOA
#define IRQ_Pin GPIO_PIN_0
#define IRQ_GPIO_Port GPIOB
#define IRQ_EXTI_IRQn EXTI0_IRQn
#define A1_Pin GPIO_PIN_12
#define A1_GPIO_Port GPIOB
#define A2_Pin GPIO_PIN_13
#define A2_GPIO_Port GPIOB
#define A3_Pin GPIO_PIN_14
#define A3_GPIO_Port GPIOB
#define A4_Pin GPIO_PIN_15
#define A4_GPIO_Port GPIOB
#define CE_Pin GPIO_PIN_8
#define CE_GPIO_Port GPIOA
#define RST_Pin GPIO_PIN_6
#define RST_GPIO_Port GPIOB
#define IRQ_SX1278_Pin GPIO_PIN_8
#define IRQ_SX1278_GPIO_Port GPIOB
#define IRQ_SX1278_EXTI_IRQn EXTI9_5_IRQn
#define DQ_Pin GPIO_PIN_9
#define DQ_GPIO_Port GPIOB
/* USER CODE BEGIN Private defines */

/* USER CODE END Private defines */

#ifdef __cplusplus
}
#endif

#endif /* __MAIN_H */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
