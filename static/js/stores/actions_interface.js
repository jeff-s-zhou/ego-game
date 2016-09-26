/**
 * Created by Jeffrey on 9/21/2016.
 */

//uses composition? maybe...just inheritance
//
export class ActionsInterface {
    selected: ActionInterface;

    get action_ids() {

    }

    get actions(): ActionInterface[] {

    }

    get targets(): any[] {

    }
}


export class ActionInterface {
    is_selected;
    valid;

    constructor() {
        this.valid = false;
    }

    selected() {

    }

    get text():string {

    }
}