import useApiRequest from "app/hooks/useApiRequest.ts";
import api from "app/api";

export default function useOnDownload({url}: {url: string}) {
    const {trigger, isLoading, isSuccess} = useApiRequest({
        apiHook: api.useDownloadAlikeMediaMutation,
        notifyIfSucceed: true,
        successMessage: "Image downloaded successfully"
    });

    const onDownload = () => {
        trigger({downloadAlikeMediaBody: {url}});
    };

    return {
        onDownload,
        isProcessing: isLoading,
        isDownloaded: isSuccess,
    };
}
