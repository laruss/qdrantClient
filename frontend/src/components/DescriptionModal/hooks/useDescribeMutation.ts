import useApiRequest from "app/hooks/useApiRequest.ts";
import api from "app/api";

export default function useDescribeMutation() {
    const {trigger, isLoading, data, isSuccess} = useApiRequest({
        apiHook: api.useDescribeMediaMutation,
        notifyIfSucceed: true,
        successMessage: "Image described successfully",
    });

    return {
        describe: trigger,
        isDescribing: isLoading,
        description: data,
        isDescribed: isSuccess,
    };
}
