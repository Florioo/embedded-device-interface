
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>

#include <pb_decode.h>
#include <pb_encode.h>

#include "eros.h"
#include "interface.pb.h"
#include "odin.h"
#include "srv_logging.h"
#include "handlers.h"

static const char *TAG = "device_api";

typedef struct
{
  Message *response;
  eros_id_t source;
} message_callback_data_t;

static int encode_response(Message *response, pb_ostream_t *output_stream);
static int decode_request(pb_istream_t *input_stream, Message *request_message,
                          message_callback_data_t *callback_data);
static bool pre_process_callback(pb_istream_t *stream, const pb_field_t *field,
                                 void **arg);

const ODIN_parameter_group_t *device_api_odin_group;

void device_api_init(ODIN_parameter_group_t *group)
{
  device_api_odin_group = group;
}


int device_api_process_stream(eros_id_t source, pb_istream_t *input_stream,
                              pb_ostream_t *output_stream)
{

  Message response = Message_init_zero;
  int status_code = StatusCodeEnum_SUCCESS;

  message_callback_data_t callback_data = {
      .response = &response,
      .source = source,
  };

  Message request_message = Message_init_zero;
  request_message.cb_content.funcs.decode = pre_process_callback;
  request_message.cb_content.arg = &callback_data;

  // Decode message
  status_code = decode_request(input_stream, &request_message, &callback_data);

  // If we encoded a message we can early return
  if (status_code != StatusCodeEnum_SUCCESS && request_message.which_content != 0)
  {
    return encode_response(&response, output_stream);
  }

  status_code = post_decode_handlers(&request_message, &response);

  if (status_code != StatusCodeEnum_SUCCESS && request_message.which_content == 0)
  {
    LOG_ERR(TAG, "Error processing message %d", status_code);
    return status_code;
  }

  int ret =  encode_response(&response, output_stream);
  return ret;
}

static bool pre_process_callback(pb_istream_t *stream, const pb_field_t *field,
                                 void **arg)
{
  Message *message = field->message;
  message_callback_data_t *callback_data = *arg;
  // int status_code = StatusCodeEnum_SUCCESS;
  
  return pre_decode_handlers(message,field, callback_data->response);

}

int device_api_process(eros_id_t source, const uint8_t *buffer, size_t size,
                       uint8_t *output_buffer, size_t output_size,
                       size_t *bytes_written)
{

#if 0
  print_hexdump(ANSI_BBLU "Request" ANSI_RESET, buffer, size);
#endif

  pb_istream_t input_stream = pb_istream_from_buffer(buffer, size);
  pb_ostream_t output_stream =
      pb_ostream_from_buffer(output_buffer, output_size);

  int ret = device_api_process_stream(source, &input_stream, &output_stream);

  // Print output
#if 0
  if (output_stream.bytes_written == 0)
  {
    printf(ANSI_BBLK "No response" ANSI_RESET "\n");
  }
  else
  {
    print_hexdump(ANSI_BGRN "Response" ANSI_RESET, output_buffer,
                  output_stream.bytes_written);
  }
#endif

  *bytes_written = output_stream.bytes_written;
  return ret;
}

static int encode_response(Message *response, pb_ostream_t *output_stream)
{
  if (!pb_encode(output_stream, Message_fields, response))
  {
    LOG_ERR(TAG, "Error encoding response: %s", PB_GET_ERROR(output_stream));
    return StatusCodeEnum_GENERAL_ERROR;
  }
  return StatusCodeEnum_SUCCESS;
}

static int decode_request(pb_istream_t *input_stream, Message *request_message,
                          message_callback_data_t *callback_data)
{
  if (!pb_decode(input_stream, Message_fields, request_message))
  {
    LOG_ERR(TAG, "Error decoding request_message: %s",
            PB_GET_ERROR(input_stream));
    return StatusCodeEnum_GENERAL_ERROR;
  }

  return StatusCodeEnum_SUCCESS;
}
