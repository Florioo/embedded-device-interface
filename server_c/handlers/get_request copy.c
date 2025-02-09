
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
  // const ODIN_parameter_group_t *parameter_group;
  // odin_access_group_t access_group;
  GetRequest *request;
  GetResponse *response;
} get_request_operation_t;

extern ODIN_parameter_group_t *device_api_odin_group;
static bool key_value_encode(pb_ostream_t *stream, const pb_field_t *field, void *const *arg);
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
    ODIN_parameter_t *parameter = ODIN_get_parameter_by_id(device_api_odin_group, operation->request->keys[key_index], 0);
    if (parameter == NULL)
    {
      printf("Failed to find parameter with id %ld\n", operation->request->keys[key_index]);
      return false;
    }

    // Read parameter
    uint8_t buffer[128];
    int size = ODIN_parameter_read_into_buffer(parameter, buffer, sizeof(buffer), ODIN_ACCESS_GROUP_INTERNAL);
    if (size < 0)
    {
      printf("Failed to read parameter\n");
      return false;
    }

    KeyValueStatus key_value_status = KeyValueStatus_init_zero;
    key_value_status.key = operation->request->keys[key_index];
    key_value_status.has_value = true;
    key_value_status.value.size = size;
    memcpy(key_value_status.value.bytes, buffer, size);

    if (!pb_encode_tag_for_field(stream, field))
    {
      printf("Failed to encode tag\n");
      return false;
    }

    if (!pb_encode_submessage(stream, KeyValueStatus_fields, &key_value_status))
    {
      printf("Failed to encode submessage\n");
      return false;
    }
  }

  return true;
}