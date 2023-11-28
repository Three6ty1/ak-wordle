import { useSubmit } from "@remix-run/react";
import React from 'react';
import { ICON_DIR, OPERATOR_RESULTS } from "~/helper/helper";
import ResultIcon from "./resultIcon";

type Props = {
    op: [string, string, number],
    hasGuessed: boolean,
}

export default function Result({op, hasGuessed}: Props) {
    let submit = useSubmit();
    const [_hasGuessed, setHasGuessed] = React.useState(hasGuessed);
    const [icon, setIcon] = React.useState<string>();

    const handleSubmit = (event: React.MouseEvent) => {
        event.preventDefault();

        setHasGuessed(true);
        hasGuessed = true;

        const guesses  = localStorage.getItem('guesses');
        let data = {
            'operator-guess': event.currentTarget.textContent,
            'guesses': guesses ? guesses : JSON.stringify([]),
        };
        submit(data, {method: 'POST'});
    }

    let url;

    if (op[OPERATOR_RESULTS.rarity] > 3) {
        url = ICON_DIR + op[OPERATOR_RESULTS.charId] + '_2.png'
    } else {
        url = ICON_DIR + op[OPERATOR_RESULTS.charId] + '.png'
    }

    return (
        <div className='flex flex-row self-center'>
            <ResultIcon image={url} alt={`${op[0]} operator icon`}/>
            <div style={{'color': hasGuessed ? 'pink' : 'black'}} onClick={(e) => handleSubmit(e)}>{op[OPERATOR_RESULTS.name]}</div> 
        </div>
    );
}