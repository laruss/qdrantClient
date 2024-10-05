import { useSelector } from 'react-redux';
import {
    selectAuthorizationModal,
    selectDescriptionModal,
    selectDialog,
    selectDuplicatesModal,
    selectLookAlikesModal,
    selectSpinnerModal,
} from 'app/slices/appSlice.ts';

export default function useAnyModalIsOpen() {
    const authorization = useSelector(selectAuthorizationModal);
    const description = useSelector(selectDescriptionModal);
    const dialog = useSelector(selectDialog);
    const duplicates = useSelector(selectDuplicatesModal);
    const lookAlikes = useSelector(selectLookAlikesModal);
    const spinnerModal = useSelector(selectSpinnerModal);

    return (
        description.isOpen ||
        authorization.isOpen ||
        dialog.isOpen ||
        duplicates.isOpen ||
        lookAlikes.isOpen ||
        spinnerModal.isOpen
    );
}
