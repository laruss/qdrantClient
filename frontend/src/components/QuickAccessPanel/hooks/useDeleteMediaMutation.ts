import useApiRequest from "app/hooks/useApiRequest.ts";
import api from "app/api";

export default function useDeleteMediaMutation() {
    const {trigger, isLoading, isSuccess} = useApiRequest({
        apiHook: api.useDeleteMediaMutation,
        notifyIfSucceed: true,
        successMessage: 'Media deleted successfully',
    });

    return {
        deleteMediaTrigger: trigger,
        mediaIsDeleting: isLoading,
        mediaIsDeleted: isSuccess,
    };
}
