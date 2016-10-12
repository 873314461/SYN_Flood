import { Component, OnInit } from '@angular/core';

import { SYN } from './data';
import { DataService } from './data.service'

@Component({
	selector: 'my-app',
	templateUrl: "app/app.component.html",
	styleUrls: ['app/app.component.css']
})
export class AppComponent implements OnInit {
	title = "请求列表";
	datas: SYN[];
	private page: number;

	constructor(
		private dataService: DataService,
	) { }

	getDatas(num: number): void {
		var pageNum = this.page;
		if (num == 1) {
			pageNum++;
			this.page = pageNum;
		} else if (num == -1) {
			pageNum--;
			if (pageNum < 1) {
				pageNum = 1;
			}
			this.page = pageNum;
		}
		this.dataService.getDatas(pageNum)
			.then(result => this.datas = result)
			.catch(this.handleError);
	}
	ngOnInit(): void {
		this.page = 1;
		this.getDatas(0);
	}

	private handleError(error: any): Promise<any> {
		console.error('An error occurred', error); // for demo purposes only
		return Promise.reject(error.message || error);
	}
}
