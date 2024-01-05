
import { GuessType } from '~/helper/helper';
import Result from './result';

type Props = {
    results: GuessType[];
    guesses: string[];
}

export default function ResultsBox({results, guesses} : Props) {
    return (
        <>
            {results.length > 0 &&
                <div className='z-30 flex flex-col max-h-[50vh] overflow-y-scroll w-1/2 my-2 py-2 rounded-md bg-base-100 shadow-sm shadow-neutral-content no-scrollbar'>
                    {results.map((op, index) => {
                        if (guesses.includes(op[0])) {
                            return <Result key={index} op={op} hasGuessed={true} />
                        } else {
                            return <Result key={index} op={op} hasGuessed={false} />
                        }
                    })}
                </div>
            }
        </>
        
    );
}