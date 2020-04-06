/*
 * hw_crc32.h
 *
 *  Created on: 
 *      Author: a.spitsyn
 */
#include "stm32f1xx_hal.h"
#ifndef HW_CRC32_H_
#define HW_CRC32_H_

//--------------------------------------------------

uint32_t HW_CRC32(const uint8_t* pData, size_t count, uint32_t init);

//--------------------------------------------------

#endif /* HW_CRC32_H_ */

