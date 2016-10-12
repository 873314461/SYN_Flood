import { Injectable } from '@angular/core';
import { Headers, Http } from '@angular/http';

import 'rxjs/add/operator/toPromise';

import { SYN } from './data';

@Injectable()
export class DataService {

    private headers = new Headers({ 'Content-Type': 'application/json' });
    private dataUrl = 'http://localhost/query';  // URL to web api
    constructor(private http: Http) { }

    getDatas(page:number):Promise<SYN[]>{
        var url = this.dataUrl +  "?page=" + page.toString();
        return this.http.get(url)
            .toPromise()
            .then(response => response.json() as SYN[])
            .catch(this.handleError);
    }

    private handleError(error: any): Promise<any> {
        console.error('An error occurred', error); // for demo purposes only
        return Promise.reject(error.message || error);
    }


}
