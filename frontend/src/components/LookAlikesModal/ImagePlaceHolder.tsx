import {Card, Skeleton} from "@nextui-org/react";

const items = [
    'w-60',
    'w-40',
    'w-80',
    'w-20',
    'w-30',
] as const;

function randomChoice(arr: typeof items) {
    return arr[Math.floor(arr.length * Math.random())];
}

export default function ImagePlaceHolder() {
    return (
        <div className='max-h-90 max-w-90'>
            <Card className={`${randomChoice(items)} h-90`}>
                <Skeleton className='w-full h-full' />
            </Card>
        </div>
    );
}
