import {Chip, Select, SelectItem} from "@nextui-org/react";
import {useMemo} from "react";

type DescriptionSelectProps = {
    label: string;
    isDisabled?: boolean;
    value: Array<string>;
    onChange: (values: Array<string>) => void;
};

export default function DescriptionSelect({label, value, onChange, isDisabled}: DescriptionSelectProps) {
    const items = useMemo(() => (value.map((item) => ({
        key: item,
        value: item,
    }))), [value]);

    return (
        <Select
            items={items}
            label={label}
            isMultiline
            isDisabled={isDisabled}
            variant="bordered"
            selectionMode="multiple"
            placeholder={`Select ${label}...`}
            className='w-full'
            selectedKeys={value}
            onSelectionChange={(keys) => {
                // keys object is set
                const newValue = (keys as Set<string>).values();
                onChange(Array.from(newValue));
            }}
            // onChange={(e) => {console.log(e)}}
            renderValue={(items) => (
                <div className='flex flex-wrap gap-1'>
                    {items.map((item) => (
                        <Chip key={item.key} className='flex flex-inline'>
                            {item.data!.value}
                        </Chip>
                    ))}
                </div>

            )}
        >
            {(item) => (
                <SelectItem key={item.key} textValue={item.value}>
                    {item.value}
                </SelectItem>
            )}
        </Select>
    );
}
