import {useSelector} from "react-redux";
import {selectConfig, selectCurrentMediaData} from "app/slices/appSlice.ts";
import {ControlPanelDataType} from "../types.ts";

type UseControlData = () => ControlPanelDataType | null;

const useControlData: UseControlData = () => {
    const currentData = useSelector(selectCurrentMediaData);
    const config = useSelector(selectConfig);

    if (!currentData || !config) {
        return null;
    }

    const [fileName, fileExtension] = currentData.file_name.split('.');

    return {
        fileName,
        fileExtension,
        isDescribed: currentData.description ? 'yes' : 'no',
        currentDataType: config.currentDataType!,
    };
}

export default useControlData;
