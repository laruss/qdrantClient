import { useDispatch, useSelector } from 'react-redux';
import { selectLookAlikesModal, setLookAlikesModalIsOpen } from 'app/slices/appSlice.ts';
import { useCallback } from 'react';

export default function useLookAlikesModalState() {
    const dispatch = useDispatch();
    const state = useSelector(selectLookAlikesModal);

    const onOpenChange = useCallback(
        (isOpen: boolean) => {
            dispatch(setLookAlikesModalIsOpen(isOpen));
        },
        [dispatch]
    );

    return {
        isOpen: state.isOpen,
        onOpenChange,
    };
}
