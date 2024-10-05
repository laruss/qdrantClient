import useApiRequest from "app/hooks/useApiRequest.ts";
import api from "app/api";

export default function useSetDescriptionMutation() {
    const {trigger, isSuccess, isLoading} = useApiRequest({
        apiHook: api.useSetDescriptionMutation,
        notifyIfSucceed: true,
        successMessage: "Description updated successfully",
    });

    return {
        saveDescription: trigger,
        isDescriptionSaved: isSuccess,
        isDescriptionSaving: isLoading,
    };
}
