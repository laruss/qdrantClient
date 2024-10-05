import useApiRequest from "app/hooks/useApiRequest.ts";
import api from "app/api";
import {useEffect} from "react";

export default function useDownloadAllImagesDataMutation() {
    const {trigger: trigger, data, isSuccess, isFetching, isError} = useApiRequest({
        apiHook: api.useLazyDownloadAllImagesDataQuery,
        notifyIfSucceed: true,
        successMessage: 'All images have been downloaded',
    });

    useEffect(() => {
        if (data) {
            const blob = new Blob([JSON.stringify(data)], {type: 'application/json'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.target = '_blank';
            a.download = 'images.json';
            a.click();
        }
    }, [data, isSuccess]);

    return {
        downloadAllData: trigger,
        isDownloading: isFetching,
        isDownloaded: isSuccess,
        isError,
    };
}
