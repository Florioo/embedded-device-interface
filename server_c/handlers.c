#include "handlers.h"
#include "srv_logging.h"

static const char *TAG = "device_api";

int pre_decode_handlers(Message *request, const pb_field_t *field, Message *response)
{

    switch (request->which_content)
    {
    case Message_set_request_tag:
        handle_set_request((SetRequest *)field->pData, response);
        break;
    }

    return true;
}

int post_decode_handlers(Message *request, Message *response)
{
    switch (request->which_content)
    {

    case Message_set_request_tag:

        // Remove response if not ack is needed
        if (!request->content.set_request.ack_required && response->which_content == Message_set_response_tag && response->content.set_response.success)
        {
            response->which_content = 0;
        }

        break;

    case Message_get_request_tag:
        handle_get_request(&request->content.get_request, response);
        break;

    default:
        LOG_ERR(TAG, "Unknown message type %d", request->which_content);
        return StatusCodeEnum_GENERAL_ERROR;
    }

    return StatusCodeEnum_SUCCESS;
}