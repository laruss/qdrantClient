import {Button, Tooltip} from "@nextui-org/react";
import {ControlPanelButtonProps} from "components/ControlPanel/types.ts";

export default function ControlPanelButton({tooltip, icon: Icon, color, label, onPress}: ControlPanelButtonProps) {
    return (
        <Tooltip content={tooltip}>
            <div>
                <Button className='h-14' onPress={onPress}>
                    <Icon color={color}/> {label}
                </Button>
            </div>
        </Tooltip>
    );
}
