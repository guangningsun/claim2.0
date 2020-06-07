<template>
	<view style="padding-bottom: 120upx;">
		<cu-custom bgColor="bg-gradual-blue" :isBack="true">
			<block slot="content">提交订单</block>
		</cu-custom>
		
		<view class="cu-card">
			<view class="cu-item">
				<form>
					<view class="cu-form-group ">
						<view class="title">部门</view>
						<text class="text-right">{{apart_name}}</text>
					</view>
					<view class="cu-form-group ">
						<view class="title">姓名</view>
						<text class="text-right">{{name}}</text>
					</view>
					<view class="cu-form-group ">
						<view class="title">电话</view>
						<text class="text-right">{{tel}}</text>
					</view>
					<view class="cu-form-group ">
						<view class="title">超限提示</view>
						<text class="text-right">{{exceed_hint}}</text>
					</view>
					
					<view class="cu-form-group">
						<text class="title">超限原因</text>
						<input
							placeholder="请填写超限原因"
							name="input"
							class="text-right"
							v-model="exceed_reason"
						/>
					</view>
					
					<view class="cu-form-group ">
						<view class="title">是否专项申请</view>
						<switch class="radius blue" @change="SwitchIsSpeciall" :class="switchIsSpeciall?'checked':''" :checked="switchIsSpeciall?true:false"></switch>
					</view>
					
				</form>
				
				<view class="cu-form-group solid-top">
					<text class="title">
						申请依据(线下申请单拍照)
					</text>
					<view class="action">
						{{imgList.length}}/1
					</view>
				</view>
				<view class="margin-left margin-bottom-sm">
					<view class="grid col-4 grid-square flex-sub">
						<view class="bg-img" v-for="(item,index) in imgList" :key="index" @tap="ViewImage" :data-url="imgList[index]">
							<image :src="imgList[index]" mode="aspectFill"></image>
							<view class="cu-tag bg-red" @tap.stop="DelImg" :data-index="index">
								<text class='cuIcon-close'></text>
							</view>
						</view>
						<view class="solids" @tap="ChooseImage" v-if="imgList.length<1">
							<text class='cuIcon-cameraadd'></text>
						</view>
					</view>
				</view>
			</view>
			
		</view>
		
		<view class="cu-card" v-for="(item, index) in order_item_list" :key="index">
			<view class="cu-item" style="margin-bottom: -10upx;">
				<view class="margin-top margin-left text-light-blue">{{item.selected_supplier_name}}</view>
				<view class=" cu-list menu-avatar" style="margin-bottom: -10upx;">
					<view class="cu-item padding-left" style="height: 200upx;">
						<view
							class="cu-avatar xl margin-left-sm"
							:style="
								item.asset_image === null
									? 'background-image:url(../../static/default.png);'
									: 'background-image:url(' +
									  domain +
									  item.asset_image +
									  ');'
							"
						></view>
						<view class="content4" style="width: calc(100% - 220upx);">
							<view class="flex justify-between">
								<view class="title">{{ item.asset_name }}</view>
								<view class="title text-orange">￥{{item.total_price}}</view>
							</view>
							
							<view class="flex">
								<view class="text-grey text-df flex">
										规格:{{ item.asset_specification }}
									</text>
								</view>
								<view class="text-grey text-df flex">
									<text class="text-cut margin-left-xs">
										| 型号:{{ item.asset_type }}
									</text>
								</view>
							</view>
				
							<view class="flex">
								<view class="text-grey text-df margin-right-sm">
									品牌: {{ item.asset_band }}
								</view>
								<view class="text-grey text-df">
									| 数量:{{item.number}}
								</view>
							</view>
						</view>
					</view>
				</view>
			</view>
		</view>
		
		<view class="box">
			<view class="cu-bar mytabbar foot tabbar bg-white">
				
				<!-- <view class="flex">
					<view class="flex-sub bg-grey padding-sm margin-xs radius">1</view>
					<view class="flex-sub bg-grey padding-sm margin-xs radius">1</view>
				</view> -->
				
				<view class="flex justify-between align-center">
					<view class="flex">
						<view class="text-df align-center margin">
							部门余额: {{apartment_balance}}元
						</view>
						<view class="text-df align-center margin">
							本单合计：￥{{totalPrice}}
						</view>
					</view>
					
					<view class="margin radius">
						<view class="cu-btn bg-light-blue round" @tap="submit">提交</view>
					</view>
				</view>
			</view>
		</view>
		
	</view>
</template>

<script>
export default {
	data() {
		return {
			apartment_balance:'',
			apartment_name:'',
			apartment_id:'',
			
			imgList: [],
			
			switchIsSpeciall:true,
			
			order_item_list:[],
			
			exceed_reason:'',
			tel:uni.getStorageSync(getApp().globalData.key_phone_num),
			apart_name:'',
			name:uni.getStorageSync(getApp().globalData.key_user_name),
			
			totalPrice:0,
			balance:this.apartment_balance - this.totalPrice,
			
			exceed_hint:'无',
			is_exceed:false,
			is_item_price_exceed:false,
			
			imgFileList:[],
			
			imageFile:null,
		};
	},
	onLoad() {
		this.order_item_list = getApp().globalData.cart_list_info;
		
		var itemList = this.order_item_list.filter(item => {
			return item.number > 0;
		});
		
		this.order_item_list = itemList;
		
		console.log(this.order_item_list);
		
		let sum = 0;
		for (var i = 0; i < this.order_item_list.length; i++) {
			console.log(this.order_item_list[i]);
			sum += this.order_item_list[i].total_price;
		}
		this.totalPrice = sum;
		this.requestBalance();
		
		
		let exceedItmeList = this.order_item_list.filter(item => {
			return item.is_exceed;
		});
		
		if(exceedItmeList.length > 0){
			this.is_exceed = true;
			this.exceedHint += '单价超限。'
			this.is_item_price_exceed = true;
		}
	},
	onHide() {
		
	},
	onShow() {

	},
	methods: {
		
		successCb(rsp) {

			if (rsp.data.error === 0) {
				console.log(rsp.data);
				var aparInfo = rsp.data.msg.budget_info[0];
				this.apartment_balance = aparInfo.surplus;
				this.apart_name = aparInfo.category_name;
				this.apart_id = aparInfo.category;
				
				this.balance = this.apartment_balance - this.totalPrice;
				
				if(this.totalPrice > this.apartment_balance){
					this.is_exceed = true;
					this.exceedHint = '总价超过部门余额。'
				}
			}
		},
		failCb(err) {
			console.log('get_apartment_balance failed', err);
		},
		completeCb(rsp) {},
		
		requestBalance() {
			this.requestWithMethod(
				getApp().globalData.get_apartment_balance + uni.getStorageSync(getApp().globalData.key_cat),
				'GET',
				'',
				this.successCb,
				this.failCb,
				this.completeCb
			);
		},
		//////////////////////
		
		ViewImage(e) {
			uni.previewImage({
				urls: this.imgList,
				current: e.currentTarget.dataset.url
			});
		},
		DelImg(e) {
			uni.showModal({
				title: '删除照片',
				content: '确定要删除这张照片吗？',
				cancelText: '否',
				confirmText: '是',
				success: res => {
					if (res.confirm) {
						this.imgList.splice(e.currentTarget.dataset.index, 1)
					}
				}
			})
		},
		ChooseImage() {
			uni.chooseImage({
				count: 1, //默认9
				sizeType: ['original', 'compressed'], //可以指定是原图还是压缩图，默认二者都有
				sourceType: ['album', 'camera'],
				success: (res) => {
					console.log(res);
					
					if (this.imgList.length != 0) {
						this.imgList = this.imgList.concat(res.tempFilePaths);
						this.imgFileList = this.imgFileList.concat(res.tempFiles);
					} else {
						this.imgList = res.tempFilePaths;
						this.imgFileList = res.tempFiles;
					}
					
					console.log(this.imgFileList);
					
					// var test = document.getElementById('test');
					// test.addEventListener('change', function() {
					// 	var t_files = this.files;
					// 	var str = '';
					// 	for(var i = 0, len = t_files.length; i < len; i++) {
					// 		console.log(t_files[i]);
					// 		str += '<a href="javascript:void(0)">' + t_files[i].name + '</a><br/>';
					// 	};
					// 	document.getElementById('content').innerHTML = str;
					// }, false);
				}
			});
		},
		SwitchIsSpeciall(e) {
			this.switchIsSpeciall = e.detail.value
		},
		
		//////////
		
		successCallback(rsp) {
			console.log(rsp);
			if (rsp.data.error === 0) {
				uni.showToast({
					title:'提交成功',
					success() {
						uni.navigateTo({
							url:'../category/category'
						})
					}
				})
				getApp().globalData.cart_list_info = [];
			}
		},
		failCallback(err) {
			uni.hideLoading();
			console.log('api_device_opt failed', err);
		},
		completeCallback(rsp) {},
		
		submit(){
			if(this.switchIsSpeciall == undefined){
				this.showToast('确定是否为专项申请？');
				return;
			}
			
			let orderItem = getApp().globalData.cart_list_info;
			console.log(orderItem);
			
			if(this.is_item_price_exceed){
				if(this.isEmpty(this.exceed_reason) || this.imgList.length == 0){
					this.showToast("单价超限，请填写超限原因及拍照");
					return;
				}
			}
			
			if(this.totalPrice > this.apartment_balance){
				if(this.isEmpty(this.exceed_reason) || this.imgList.length == 0){
					this.showToast("总价超过部门余额，请填写超限原因及拍照");
					return;
				}
			}
			
			if(this.switchIsSpeciall){
				if(this.isEmpty(this.exceed_reason) || this.imgList.length == 0){
					this.showToast("专项申请，请填写超限原因及拍照");
					return;
				}
			}
			
			uni.showLoading({
				title: '正在提交订单',
			})
			
			console.log(this.imgList);
			
			// uni.uploadFile({
			// 	url: getApp().globalData.image_upload_url,
			// 	filePath: this.imgList[0],
			// 	name: 'file',
			// 	success: (uploadFileRes) => {
			// 		console.log("upload:");
			// 		console.log(uploadFileRes.data);
			// 	}
			// });
			
			var itemList = [];

			let newArr = orderItem.map((item) => {
				return Object.assign({ item_sn: item.asset_sn },
				{item_supplier_id:item.selected_supplier},
				{item_num:item.number},
				{item_price:item.total_price});
			});
			itemList = newArr;
		
			
			let params = {
				weixin_openid:uni.getStorageSync( getApp().globalData.key_wx_openid),
				order_apartment: this.apart_id,
				order_exceed_reason: this.exceed_reason,
				order_is_special:this.switchIsSpeciall ? 'True' : 'False',
				order_image:'',
				order_item_list:JSON.stringify(itemList),
				order_total_price:this.totalPrice,
				is_exceed: this.is_exceed ? 'True' : 'False'
			};

			if(this.imgList.length > 0){
				uni.uploadFile({
					url: getApp().globalData.get_submit_order,
					filePath: this.imgList[0],
					name: 'file',
					formData: params,
					success: (uploadFileRes) => {
						// this.successCallback(uploadFileRes);
						console.log('upload success');
						console.log(uploadFileRes);
					},
					fail: (res) => {
						console.log('upload failed');
					}
				});
			}else{
				this.requestWithMethod(
					getApp().globalData.get_submit_order,
					"POST",
					params,
					this.successCallback,
					this.failCallback,
					this.completeCallback);
			}
		},
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
