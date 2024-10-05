import { useSelector } from 'react-redux';
import { selectConfig } from 'app/slices/appSlice.ts';
import useApiRequest from 'app/hooks/useApiRequest.ts';
import api from 'app/api';

type PromptItems = [string[], (promptItems: string[]) => void];

export default function usePromptItems(): PromptItems {
    const config = useSelector(selectConfig);

    const { trigger } = useApiRequest({
        apiHook: api.useSetPromptPartsMutation,
    });

    return [
        config?.promptParts || [],
        (promptItems: string[]) => {
            trigger({ setPromptPartsPayload: { parts: promptItems } });
        }
    ];
}
