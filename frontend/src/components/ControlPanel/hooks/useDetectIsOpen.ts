import {isMobile} from 'react-device-detect';
import {useDispatch} from "react-redux";
import {useEffect} from "react";
import {setControlPanelIsOpen} from "app/slices/appSlice.ts";

export default function useDetectIsOpen() {
    const dispatch = useDispatch();

    useEffect(() => {
        if (!isMobile) {
            dispatch(setControlPanelIsOpen(true));
        }
    }, [dispatch]);
}
