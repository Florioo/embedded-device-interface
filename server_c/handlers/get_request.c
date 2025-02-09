
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>

#include <pb_decode.h>
#include <pb_encode.h>

#include "eros.h"
#include "interface.pb.h"
#include "odin.h"
#include "odin_core.h"
#include "odin_lookup.h"
#include "odin_utils.h"
#include "srv_logging.h"

typedef struct
{
  GetRequest *request;
  GetResponse *response;
} get_request_operation_t;

extern const ODIN_parameter_group_t *device_api_odin_group;
static bool key_value_encode(pb_ostream_t *stream, const pb_field_t *field, void *const *arg);
static bool encode_key_and_value(uint32_t key, uint8_t *value, size_t size, pb_ostream_t *stream, const pb_field_t *field);
static bool encode_key_and_status(uint32_t key, StatusCodeEnum code, pb_ostream_t *stream, const pb_field_t *field);

static get_request_operation_t operation;

int handle_get_request(GetRequest *request, Message *response)
{
  operation.response = &response->content.get_response;
  operation.request = request;

  response->which_content = Message_get_response_tag;
  response->content.get_response.key_value_status_pairs.funcs.encode = key_value_encode;
  response->content.get_response.key_value_status_pairs.arg = &operation;

  return StatusCodeEnum_SUCCESS;
}

static bool key_value_encode(pb_ostream_t *stream, const pb_field_t *field, void *const *arg)
{
  get_request_operation_t *operation = (get_request_operation_t *)*arg;



  for (size_t key_index = 0; key_index < operation->request->keys_count; key_index++)
  {
    // Find parameter
    const ODIN_parameter_t *parameter = ODIN_get_parameter_by_id(device_api_odin_group, operation->request->keys[key_index], 0);
    if (parameter == NULL)
    {

      if (!encode_key_and_status(operation->request->keys[key_index], StatusCodeEnum_ODIN_ERROR_PARAMETER_NOT_FOUND, stream, field))
      {
        return false;
      }

      continue;
    }

    // Read parameter
    uint8_t buffer[128];
    int ret = ODIN_parameter_read_into_buffer(parameter, buffer, sizeof(buffer), ODIN_ACCESS_GROUP_INTERNAL);
    if (ret < ODIN_SUCCESS)
    {
      if (!encode_key_and_status(operation->request->keys[key_index], ret, stream, field))
      {
        return false;
      }

      continue;
    }

    // encode key and value
    if (!encode_key_and_value(operation->request->keys[key_index], buffer, ret, stream, field))
    {
      return false;
    }
  }
  return true;
}

static bool encode_key_and_status(uint32_t key, StatusCodeEnum code, pb_ostream_t *stream, const pb_field_t *field)
{

  if (!pb_encode_tag_for_field(stream, field))
  {
    printf("Failed to encode tag\n");
    return false;
  }

  KeyValueStatus key_value_status = KeyValueStatus_init_zero;
  key_value_status.key = key;
  key_value_status.has_code = true;
  key_value_status.code = code;
  if (!pb_encode_submessage(stream, KeyValueStatus_fields, &key_value_status))
  {
    printf("Failed to encode submessage\n");
    return false;
  }
  printf("Encoded key and status: %ld - %d\n", key, code);

  return true;
}

static bool encode_key_and_value(uint32_t key, uint8_t *value, size_t size, pb_ostream_t *stream, const pb_field_t *field)
{
  if (!pb_encode_tag_for_field(stream, field))
  {
    printf("Failed to encode tag\n");
    return false;
  }

  KeyValueStatus key_value_status = KeyValueStatus_init_zero;
  key_value_status.key = key;
  key_value_status.has_value = true;
  key_value_status.value.size = size;
  memcpy(key_value_status.value.bytes, value, size);
  if (!pb_encode_submessage(stream, KeyValueStatus_fields, &key_value_status))
  {
    printf("Failed to encode submessage\n");
    return false;
  }
  printf("Encoded key and value: %ld - len: %d\n", key, size);
  return true;
}
