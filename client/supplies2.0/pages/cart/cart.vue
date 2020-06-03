<template>
	<view>
		<cu-custom bgColor="bg-gradual-blue" :isBack="true">
			<block slot="content">物品篮</block>
		</cu-custom>
		
		<view v-show="showEmpty" style="margin-top: 200upx;">
			<view class="flex justify-center align-center margin-left-xl">
				<image src="../../static/empty_icon.png" style="width: 200upx; height: 200upx;" />
			</view>
			<view class="flex justify-center text-gray margin-top">空空如也</view>
		</view>
		
		<view v-for="(item, index) in cartList" :key="index">
			<view class="cu-card card-margin">
				<view
					class="cu-item padding-sm solids"
					:class="[parseInt(item.number) > 0 ? 'line-light-blue' : '']"
				>
					<view class="flex justify-between">
						<!-- <img class="margin-left-xl" :src="domain + item.asset_image ../../static/default.png" :onerror="default_img" style="width: 150upx; height: 150upx;"></img> -->
						<view class="flex align-center">
							<img
								class=""
								:src="item.asset_image === null ? '../../static/default.png' : domain + item.asset_image"
								:onerror="default_img"
								style="width: 150upx; height: 150upx;"
							/>
							<view class="margin-left-xs">
								<view class="flex">
									<view class="title text-df margin-right-sm">
										{{ item.asset_name }} | 
									</view>
									<view class="text-orange text-df">
										单价:{{item.selected_supplier_price}}
									</view>
								</view>
								
								<view>
									<text class="text-gray margin-right-xs">
										型号: {{ item.asset_type }}
									</text>
								</view>
								<view>
									<text class="text-gray margin-right-xs">
										规格: {{ item.asset_specification }}
									</text>
								</view>
								<view>
									<text class="text-gray margin-right-xs">
										供应商: {{ item.selected_supplier_name }}
									</text>
								</view>
							</view>
						</view>

						<view class="flex align-center">
							<!-- <uni-number-box
								class="step"
								:min="0"
								:max="item.stock"
								:value="item.number > item.stock ? item.stock : item.number"
								:id="item.item_id"
								@change="numberChange($event, item, index)"
							/> -->
							<uni-number-box
								class="step"
								:min="0"
								:max="9999"
								:value="item.number > 9999 ? 9999 : item.number"
								:id="item.item_id"
								@change="numberChange($event, item, index)"
							/>
						</view>
					</view>
				</view>
			</view>
		</view>
		
		<view v-show="showNoMore" class="margin-top-xl margin-bottom-xl text-gray flex justify-center">
			----- 没有更多了 -----
		</view>
		
		<view v-show="!showEmpty">
			<uni-fab
				ref="fab"
				:pattern="pattern"
				:content="content"
				:horizontal="horizontal"
				:vertical="vertical"
				:direction="direction"
				@trigger="trigger"
			/>
		</view>
		
		<view class="cu-modal" :class="modalName=='ReasonModal'?'show':''">
			<view class="cu-dialog">
				<view class="cu-bar bg-white justify-end">
					<view class="content">数量超限申请</view>
					<view class="action" @tap="hideModal">
						<text class="cuIcon-close text-light-purple"></text>
					</view>
				</view>
				<view class="cu-item">
					<view class="flex cu-form-group">
						<view class="title">超限物品</view>
						<view class="text-wrapper text-gray text-right margin-bottom-sm margin-top-sm">
							{{ exceedHint }}
						</view>
					</view>
					<view class="cu-form-group">
						<view class="title">理由</view>
						<input class="text-left" placeholder="输入申请理由" name="input" v-model="reason"></input>
					</view>
				</view>
		
				<view class="cu-bar bg-white justify-end">
					<view class="action">
						<button class="cu-btn line-gray text-gray" @tap="hideModal">取消</button>
						<button class="cu-btn bg-light-blue margin-left" @tap="onConfirmReason()">确定</button>
					</view>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
import { uniNumberBox } from '@dcloudio/uni-ui';
import { uniFab } from '@dcloudio/uni-ui';
export default {
	components: {
		uniNumberBox,
		uniFab
	},
	data() {
		return {
			showNoMore: false,
			
			modalName: null,
			reason:'',
			
			domain: getApp().globalData.domain,
			default_img: 'this.src="' + require('../../static/default.png') + '"',

			cartList: [],
			
			showEmpty: false,
			
			exceedHint:'',

			directionStr: '垂直',
			horizontal: 'right',
			vertical: 'bottom',
			direction: 'horizontal',
			pattern: {
				color: '#7A7E83',
				backgroundColor: '#fff',
				selectedColor: '#2481c4',
				buttonColor: '#59aef9'
			},
			content: [
				{
					iconPath: '/static/submit1.png',
					selectedIconPath: '/static/submit1.png',
					text: '提交订单',
					active: true
				}
			],
			catagory_num_limit: 5,
			item_limit: 5
		};
	},
	onLoad() {
		
	},
	onHide() {
		
	},
	onShow() {
		console.log('onshow');
		this.cartList = getApp().globalData.cart_list_info;
		this.showEmpty = !(this.cartList.length > 0);
		this.showNoMore = !this.showEmpty;
	},
	methods: {
		successCb(rsp) {
			console.log('success cb');
			if (rsp.data.error === 0) {
				let repList = rsp.data.msg.asset_info;

				let newArr = repList.map((item, stock, number) => {
					return Object.assign(item, { stock: stock }, { number: 0 });
				});
				newArr.map(item => {
					item.stock = parseInt(item.asset_count);
				});
				console.log(newArr);
				this.cartList = newArr;
			}
		},
		failCb(err) {
			console.log('api_asset failed', err);
		},
		completeCb(rsp) {},

		//数量
		numberChange(event, item, index) {
			console.log('event:' + event + ', index:' + index);
			console.log(item);
			this.cartList[index].number = event;
			let temp = this.cartList[index];
			this.$set(this.cartList, index, temp);
			
			let num = parseInt(this.cartList[index].number);
			let price = parseFloat(this.cartList[index].selected_supplier_price);
			
			let totalPrice = num * price;
			console.log(totalPrice);
			this.cartList[index].total_price = totalPrice;
		},

		showModal(e) {
			this.modalName = e;
		},
		hideModal(e) {
			this.modalName = null;
		},
		
		onConfirmReason(){
			if (this.isEmpty(this.reason)) {
				this.showToast('申请理由不能为空！');
				return;
			}
			this.submit();
			this.reason = '';
		},

		trigger(e) {
			// this.exceedHint = '';
			// let itemList = this.cartList.filter(item => {
			// 	return item.number > 0;
			// });
			
			// if(itemList.length == 0){
			// 	this.showToast('请选择物品数量');
			// 	return;
			// }
		
			let itemList = this.cartList.filter(item => {
				return item.number > 0;
			});
			
			if(itemList.length == 0){
				this.showToast('请选择物品数量');
				return;
			}
			
			getApp().globalData.cart_list_info = this.cartList;
			
			uni.navigateTo({
				url:'../order/order_confirm'
			})
			
			// let isExceedLimit = false;
			// for (let i = 0; i < itemList.length; i++) { 
			// 	console.log('current number: '+this.cartList[i].number);
			// 	console.log('lim num: '+itemList[i].asset_limit_nu);
				
			//     if(itemList[i].asset_limit_nu < itemList[i].number){
			// 		isExceedLimit = true;
			// 		if(i ==  itemList.length - 1){
			// 			this.exceedHint += itemList[i].asset_name.replace(/\s*/g,"") + ' | 限领:' + itemList[i].asset_limit_nu;
			// 		}else{
			// 			this.exceedHint += itemList[i].asset_name.replace(/\s*/g,"") + ' | 限领:' + itemList[i].asset_limit_nu +'\n';
			// 		}
			// 	}
			//  }
			//  console.log(this.exceedHint);
			 
			//  if(isExceedLimit){
			// 	 this.showModal('ReasonModal');
			//  }else{
			// 	 if (e.index === 0) {
			// 	 	uni.showModal({
			// 	 		title: '提示',
			// 	 		content: '是否申领选择的物品？',
			// 	 		success: res => {
			// 	 			if (res.confirm) {
			// 	 				this.submit();
			// 	 			} else if (res.cancel) {
			// 	 				console.log('用户点击取消');
			// 	 			}
			// 	 		}
			// 	 	});
			// 	 } else if (e.index === 1) {
			// 	 	uni.navigateTo({
			// 	 		url: '../history/history'
			// 	 	});
			// 	 }
			//  }
		},

		successCallback(rsp) {
			console.log('success cb');
			if (rsp.data.error === 0) {
				uni.requestSubscribeMessage({
				  tmplIds: ['GOx_7a-j5CFw6kOHS9Z3H05LXmgNK8tudus9ud7c3ZU'],
				  success (res) {
					  console.log('subscribe msg: ');
					  console.log(res);
				  }
				})
				
				getApp().globalData.cart_list_info = [];
				
				uni.showToast({
					title: rsp.data.msg,
					complete: () => {
						// setTimeout(function() {
						// 	uni.navigateTo({
						// 		url:'../category/category_all'
						// 	})
						// }, 1500);
						uni.navigateBack();
					}
				});
			} else if (rsp.data.error === 1) {
				this.showToast(rsp.data.msg);
			}
		},
		failCallback(err) {
			uni.hideLoading();
			console.log('api_claim_asset failed', err);
			this.showToast(err);
		},
		completeCallback(rsp) {},

		getCartCataNum() {
			let result = 0;
			for (var i = 0; i < this.cartList.length; i++) {
				this.cartList[i];
			}
		},

		submit() {
			// uni.navigateTo({
			// 	url:'../order/order_confirm'
			// });
			
			// getApp().globalData.cart_list_info = 
			
			let itemList = this.cartList.filter(item => {
				return item.number > 0;
			});
			
			if(itemList.length == 0){
				this.showToast('请选择物品数量');
				return;
			}
			
			getApp().globalData.cart_list_info = itemList;
			
			uni.navigateTo({
				url:'../order/order_confirm'
			});

			// uni.showLoading({
			// 	title: '正在提交'
			// });
			
			// this.hideModal();

			// var cat = uni.getStorageSync('key_cat');
			// console.log('===cat: ',cat);
			// if(cat){
			// 	let result_list = itemList.map(item => {
			// 		return Object.assign(
			// 			{ claim_count: item.number },
			// 			{ claim_name: item.asset_name },
			// 			{ claim_unit: item.asset_unit},
			// 			{ id: item.id }
			// 		);
			// 	});
				
			// 	console.log(result_list);
				
			// 	let params = {
			// 		choose_list: JSON.stringify(result_list),
			// 		category: cat,
			// 		reason: this.reason,
			// 		claim_weixin_openid: uni.getStorageSync('key_wx_openid')
			// 	};
				
			// 	this.requestWithMethod(
			// 		getApp().globalData.api_claim_asset,
			// 		'POST',
			// 		params,
			// 		this.successCallback,
			// 		this.failCallback,
			// 		this.completeCallback
			// 	);
			// }
			// else{
			// 	this.showToast('部门号为空，请扫部门提供的二维码进行申请')
			// }
		}
	}
};
</script>

<style>
.card-margin {
	margin-top: -30upx;
}
.text-wrapper {
	white-space: pre-wrap;
}
</style>
