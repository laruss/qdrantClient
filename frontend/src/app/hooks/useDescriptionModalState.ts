import {useDispatch, useSelector} from "react-redux";
import {selectDescriptionModal, setDescriptionModalIsOpen} from "app/slices/appSlice.ts";
import {useCallback} from "react";

export default function useDescriptionModalState() {
    const dispatch = useDispatch();
    const state = useSelector(selectDescriptionModal);

    const onOpenChange = useCallback((isOpen: boolean) => {
        dispatch(setDescriptionModalIsOpen(isOpen));
    }, [dispatch]);

    return {
        isOpen: state.isOpen,
        onOpenChange,
    }
}
