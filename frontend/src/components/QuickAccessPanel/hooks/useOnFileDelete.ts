import useDialogModal from "app/hooks/useDialogModal.ts";
import useDeleteMediaMutation from "components/QuickAccessPanel/hooks/useDeleteMediaMutation.ts";
import {useEffect} from "react";
import useSpinnerModalState from "app/hooks/useSpinnerModalState.ts";

export default function useOnFileDelete() {
    const {onOpenChange: onSpinnerShow} = useSpinnerModalState();
    const {deleteMediaTrigger, mediaIsDeleting, mediaIsDeleted} = useDeleteMediaMutation();
    const {openDialog} = useDialogModal({
        title: "Delete file",
        content: "Are you sure you want to delete this file?",
    });

    useEffect(() => {
        mediaIsDeleting && onSpinnerShow(true);
    }, [mediaIsDeleting, onSpinnerShow]);

    useEffect(() => {
        mediaIsDeleted && onSpinnerShow(false);
    }, [mediaIsDeleted, onSpinnerShow]);

    return async () => {
        const confirmed = await openDialog();
        if (confirmed) {
            deleteMediaTrigger();
        }
    };
}
