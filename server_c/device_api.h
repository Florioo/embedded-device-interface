
#include "eros.h"
#include <odin.h>
#include <pb_decode.h>
#include <pb_encode.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>


int device_api_process_stream(eros_id_t source, pb_istream_t *input_stream,
                              pb_ostream_t *output_stream);

int device_api_process(eros_id_t source, const uint8_t *buffer, size_t size,
                       uint8_t *output_buffer, size_t output_size,
                       size_t *bytes_written);

void device_api_init(ODIN_parameter_group_t *group);
