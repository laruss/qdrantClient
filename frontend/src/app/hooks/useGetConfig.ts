import useApiRequest from "app/hooks/useApiRequest.ts";
import api from "app/api";
import {useEffect} from "react";

export default function useGetConfig() {
    const {trigger} = useApiRequest({
        apiHook: api.useLazyGetConfigQuery,
    });

    useEffect(() => {
        trigger();
    }, [trigger]);
}
