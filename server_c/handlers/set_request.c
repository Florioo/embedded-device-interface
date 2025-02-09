
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

extern ODIN_parameter_group_t *device_api_odin_group;

static bool key_value_decode(pb_istream_t *stream, const pb_field_t *field,
                             void **arg)
{

  Message *response = *arg;

  KeyValue key_value = KeyValue_init_zero;
  if (!pb_decode(stream, KeyValue_fields, &key_value))
  {
    printf("Error decoding key value\n");
    // Return with no response
    return false;
  }

  const ODIN_parameter_t *parameter =
      ODIN_get_parameter_by_id(device_api_odin_group, key_value.key, 0);

  // TODO: Acces control
  int odin_status = ODIN_SUCCESS;

  if (!parameter)
  {
    odin_status = ODIN_ERROR_PARAMETER_NOT_FOUND;
  }
  else
  {

    odin_status = ODIN_parameter_write(parameter, key_value.value.bytes,
                                       key_value.value.size, ODIN_ACCESS_GROUP_INTERNAL);
  }

  // Encode the response
  if (odin_status < ODIN_SUCCESS)
  {
    response->which_content = Message_set_response_tag;
    response->content.set_response.success = false;

    int keys = response->content.set_response.key_status_pairs_count++;

    if (keys >= 16)
    {
      printf("Too many keys in response\n");
      return false;
    }

    response->content.set_response.key_status_pairs[keys].key = key_value.key;
    response->content.set_response.key_status_pairs[keys].code = odin_status;
  }
  else
  {
    response->which_content = Message_set_response_tag;
    response->content.set_response.success = true;
  }

  return true;
}

int handle_set_request(SetRequest *request, Message *response)
{
  request->key_value_pairs.arg = response;
  request->key_value_pairs.funcs.decode = key_value_decode;
  return StatusCodeEnum_SUCCESS;
}
