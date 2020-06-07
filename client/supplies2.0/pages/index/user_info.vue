<template>
	<view>
		<cu-custom bgColor="bg-gradual-blue" :isBack="true">
			<block slot="content">信息登记</block>
		</cu-custom>

		<view class="cu-card">
			<view class="cu-item">
				<form>
					<view class="cu-form-group margin-top">
						<text class="cuIcon-title text-gray"></text>
						<view class="title">昵称</view>
						<input class="text-right" placeholder="请输入昵称" name="input" v-model="nickname" />
					</view>
					<view class="cu-form-group">
						<text class="cuIcon-title text-red"></text>
						<text class="title">手机号码</text>
						<input
							placeholder="请输入手机号码"
							name="input"
							class="text-right"
							@input="checkBtnEnable"
							v-model="tel_num"
							:disabled="true"
						/>
					</view>
					<view class="cu-form-group">
						<text class="cuIcon-title text-red"></text>
						<text class="title">姓名</text>
						<input
							placeholder="请填写真实姓名,以便管理员审核"
							name="input"
							class="text-right"
							@input="checkBtnEnable"
							v-model="user_name"
						/>
					</view>
					<!-- <view class="cu-form-group">
						<text class="cuIcon-title text-red"></text>
						<text class="title">部门</text>
						<input placeholder="请选择您所在部门" name="input" v-model="apartment"></input>
					</view> -->
					<view class="cu-form-group">
						<text class="cuIcon-title text-red"></text>
						<text class="title">部门</text>
						<picker
							@change="apartPickerChange"
							:value="apartment_picker_index"
							:range="apartment_picker"
						>
							<view class="picker">
								{{
									apartment_picker_index > -1
										? apartment_picker[apartment_picker_index]
										: '请选择所属部门'
								}}
							</view>
						</picker>
					</view>
					<view class="cu-form-group">
						<text class="cuIcon-title text-gray"></text>
						<view class="title">物品送达常用地址</view>
						<input
							placeholder="选填,请填写工作地点具体门牌号"
							name="input"
							class="text-right"
							v-model="address"
						/>
					</view>
				</form>
			</view>

			<view class="justify-between bottom-box">
				<view class="padding flex flex-direction">
					<button class="cu-btn bg-blue lg" :disabled="btn_disabled" @click="onSubmit">
						提交
					</button>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
export default {
	data() {
		return {
			nickname: '',
			tel_num: '',
			user_name: '',
			apartment: '',
			address: '',
			apartment_picker_index: -1,
			apartment_picker: [],
			apartment_info_list:[],

			btn_disabled: true,
			apartment_id: -1
		};
	},

	onLoad() {
		this.requestApartment();
		this.tel_num = uni.getStorageSync(getApp().globalData.key_phone_num);
	},

	methods: {
		requestApartment() {
			this.requestWithMethod(
				getApp().globalData.api_get_apartment_list,
				'GET',
				'',
				this.successCb,
				this.failCb,
				this.completeCb
			);
		},
		successCb(rsp) {
			if (rsp.data.error === 0) {
				this.apartment_info_list = rsp.data.msg.category_info;
				console.log(this.apartment_info_list);

				var apartments = this.apartment_picker;
				this.apartment_info_list.map(function(item) {
					apartments.push(item.name);
				});
				console.log("==apart==");
				console.log(apartments);
			}
		},
		failCb(err) {
			console.log('api_apartment_list failed', err);
		},
		completeCb(rsp) {},

		////////////////////

		apartPickerChange(e) {
			this.apartment_picker_index = parseInt(e.detail.value);
			if (this.apartment_picker_index === -1) {
				this.apartment_picker_index = 0;
			} else {
				this.apartment_picker_index = parseInt(e.detail.value);
			}
			this.checkBtnEnable();
			
		},
		checkBtnEnable() {
			if (
				this.date == '' ||
				this.apartment_picker[this.apartment_picker_index] == '' ||
				this.apartment_picker[this.apartment_picker_index] == undefined ||
				this.isEmpty(this.tel_num) ||
				this.isEmpty(this.user_name)
			) {
				this.btn_disabled = true;
			} else {
				this.btn_disabled = false;
			}
		},
		onSubmit(){
			if (this.apartment_picker[this.apartment_picker_index] !== undefined) {
			    this.apartment = this.apartment_picker[this.apartment_picker_index];
			}
			
			uni.showLoading({
				title: '正在提交信息',
			})
			
			let info = this.apartment_info_list[this.apartment_picker_index];
			let apart_id = info.id;
			this.apartment_id = apart_id;
			
			uni.setStorageSync(getApp().globalData.key_user_name,this.user_name);
			
			let params = {
				openid: uni.getStorageSync(getApp().globalData.key_wx_openid),
				nickname: this.nickname,
				username: this.user_name,
				address: this.address,
				apartment: apart_id
			};
			
			this.requestWithMethod(
				getApp().globalData.api_submit_user_info,
				"POST",
				params,
				this.successCallback,
				this.failCallback,
				this.completeCallback);
		},
		successCallback(rsp) {
			uni.hideLoading();
			if (rsp.data.error === 0) {
				uni.setStorageSync(getApp().globalData.key_cat,this.commoditycategory);
				uni.showToast({
					title:'提交成功'
				});
				uni.navigateTo({
					url:'../category/category'
				})
			}
		},
		failCallback(err) {
			uni.hideLoading();
			this.showToast(err);
			console.log('api_submit_user_info failed', err);
		},
		completeCallback(rsp) {},
	}
};
</script>

<style></style>
