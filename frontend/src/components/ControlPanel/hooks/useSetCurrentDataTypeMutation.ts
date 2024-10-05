import useApiRequest from "app/hooks/useApiRequest.ts";
import api from "app/api";

export default function useSetCurrentDataTypeMutation() {
    const {trigger} = useApiRequest({
        apiHook: api.useSetDataTypeMutation,
        notifyIfSucceed: true,
        successMessage: 'Data type has been changed',
    });

    return {changeDataType: trigger};
}
