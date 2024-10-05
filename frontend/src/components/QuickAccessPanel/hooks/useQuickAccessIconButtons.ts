import {TbMailFast} from "react-icons/tb";
import {FaTextSlash} from "react-icons/fa6";
import {SiQuicklook} from "react-icons/si";
import {BsTrash} from "react-icons/bs";
import useLookAlikesModalState from "app/hooks/useLookAlikesModalState.ts";
import useOnFileDelete from "components/QuickAccessPanel/hooks/useOnFileDelete.ts";
import useRemoveText from "components/QuickAccessPanel/hooks/useRemoveText.ts";
import useDescribe from "components/QuickAccessPanel/hooks/useDescribe.ts";

export default function useQuickAccessIconButtons() {
    const {onOpenChange} = useLookAlikesModalState();
    const onFileDelete = useOnFileDelete();
    const removeTextTrigger = useRemoveText();
    const describe = useDescribe();

    return [
        {
            icon: TbMailFast,
            label: 'Fast',
            tooltip: 'Fast Description',
            color: '#60bf3f',
            callback: () => describe({describeMediaPayload: {prompt: ''}}),
        },
        {
            icon: FaTextSlash,
            label: 'Text',
            tooltip: 'Remove Text',
            color: '#f7b500',
            callback: () => removeTextTrigger(),
        },
        {
            icon: SiQuicklook,
            label: 'LookAlike',
            tooltip: 'Show Look Alikes',
            color: '#3d56d6',
            callback: () => onOpenChange(true),
        },
        {
            icon: BsTrash,
            label: 'Delete',
            tooltip: 'Delete Item',
            color: '#f70000',
            callback: onFileDelete,
        },
    ] as const;
}
