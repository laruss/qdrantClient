import {useCallback} from "react";
import {useDispatch} from "react-redux";
import {selectDialog, setDialog} from "app/slices/appSlice.ts";
import {store} from "app/store.ts";

type UseDialogModalProps = {
    title: string;
    content?: string;
};

export default function useDialogModal({title, content}: UseDialogModalProps) {
    const dispatch = useDispatch();

    const openDialog = useCallback(() => {
        dispatch(setDialog({
            isOpen: true,
            title,
            content,
            confirmed: undefined,
        }));

        return new Promise<boolean>((resolve) => {
            const interval = setInterval(() => {
                const currentDialogState = selectDialog(store.getState());
                if (currentDialogState.confirmed !== undefined) {
                    clearInterval(interval);
                    resolve(currentDialogState.confirmed);
                }
            }, 100);
        });
    }, [content, dispatch, title]);

    return {openDialog};
}
