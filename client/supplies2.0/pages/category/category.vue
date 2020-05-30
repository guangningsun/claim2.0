<template>
	<view>
		<cu-custom bgColor="bg-gradual-blue" :isBack="false">
			<block slot="content">物品分类</block>
		</cu-custom>

		<view v-show="showEmpty" style="margin-top: 200upx;">
			<view class="flex justify-center align-center margin-left-xl">
				<image src="../../static/empty_icon.png" style="width: 200upx; height: 200upx;" />
			</view>
			<view class="flex justify-center text-gray margin-top">空空如也</view>
		</view>

		<view class="VerticalBox">
			<scroll-view
				class="VerticalNav nav"
				scroll-y
				scroll-with-animation
				:scroll-top="verticalNavTop"
				style="height:calc(100vh - 100upx)"
			>
				<view
					class="cu-item"
					:class="item.id == tabCur ? 'text-blue cur' : ''"
					v-for="(item, index) in catList"
					:key="index"
					@tap="TabSelect"
					:data-id="item.id"
				>
					{{ item.name }}
				</view>
			</scroll-view>
			<scroll-view
				class="VerticalMain"
				scroll-y
				scroll-with-animation
				style="height:calc(100vh - 100upx);"
				:scroll-into-view="'main-' + mainCur"
				@scroll="VerticalMain"
			>
				<view
					class="padding-top"
					v-for="(item, index) in catList"
					:key="index"
					:id="'main-' + item.id"
				>
					<view class="solid-bottom bg-white">
						<view class="text-blac padding-sm">{{ item.name }}</view>
					</view>
					<view class="cu-list menu-avatar">
						<view
							class="cu-item"
							style="height: 200upx;"
							v-for="(item2, index2) in item.asset_info"
							:key="index2"
						>
							<view
								class="cu-avatar lg"
								:style="
									item2.asset_image === null
										? 'background-image:url(../../static/default.png);'
										: 'background-image:url(' +
										  domain +
										  item2.asset_image +
										  ');'
								"
							></view>
							<view class="content2">
								<view class="flex">
									<view class="text-grey">{{ item2.asset_name }}</view>
									<view class="text-grey text-sm margin-left-xs">
										| 库存:{{ item2.asset_count }}
									</view>
								</view>

								<view class="flex">
									<view class="text-gray text-sm flex">
										<text class="text-cut">
											规格:{{ item2.asset_specification }}
										</text>
									</view>
									<view class="text-gray text-sm flex">
										<text class="text-cut margin-left-xs">
											| 型号:{{ item2.asset_type }}
										</text>
									</view>
								</view>

								<view
									v-show="
										item2.asset_limit_price !== undefined &&
											item2.asset_limit_price !== null &&
											item2.asset_limit_price !== ''
									"
									class="text-gray text-sm flex"
								>
									<text class="text-cut cu-tag line-yellow round sm">
										{{ item2.asset_limit_price }}
									</text>
								</view>

								<view class="flex">
									<view
										v-show="
											item2.asset_band !== undefined &&
												item2.asset_band !== null &&
												item2.asset_band !== ''
										"
										class="text-sm flex"
									>
										<text class="text-grey">品牌: {{ item2.asset_band }}</text>
									</view>

									<view
										class="cuIcon-cartfill round padding-xs bg-olive margin-bottom-xs"
										@tap="onAdd(item2)"
									></view>
									<view
										class="cuIcon-deletefill round padding-xs bg-orange margin-top-sm margin-bottom-xs"
										@tap="onMinus(item2)"
									></view>
								</view>
							</view>
						</view>
					</view>
				</view>
				<view
					v-show="showNoMore"
					class="margin-top-xl margin-bottom-xl text-gray "
					style="margin-left: 100upx;"
				>
					----- 没有更多了 -----
				</view>
			</scroll-view>
		</view>
		<view>
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

		<view class="cu-modal" :class="modalName == 'ChooseSupplierModal' ? 'show' : ''">
			<view class="cu-dialog">
				<view class="cu-bar bg-white justify-end">
					<view class="content">选择供应商</view>
					<view class="action" @tap="hideModal">
						<text class="cuIcon-close text-light-purple"></text>
					</view>
				</view>
				<view class="margin-top cu-list menu-avatar">
					<view class="cu-item padding-left" style="height: 250upx;">
						<view
							class="cu-avatar xl"
							:style="
								current_item_info.asset_image === null
									? 'background-image:url(../../static/default.png);'
									: 'background-image:url(' +
									  domain +
									  current_item_info.asset_image +
									  ');'
							"
						></view>
						<view class="content3">
							<view class="flex">
								<view class="text-grey">{{ current_item_info.asset_name }}</view>
								<view class="text-grey text-df margin-left-xs">
									| 库存:{{ current_item_info.asset_count }}
								</view>
							</view>

							<view class="flex">
								<view class="text-gray text-df flex">
									<text class="text-cut">
										规格:{{ current_item_info.asset_specification }}
									</text>
								</view>
								<view class="text-gray text-df flex">
									<text class="text-cut margin-left-xs">
										| 型号:{{ current_item_info.asset_type }}
									</text>
								</view>
							</view>

							<!-- <view v-show="current_item_info.notice !== undefined && current_item_info.notice !== null && current_item_info.notice !== '' " class="text-gray text-sm flex">
							<text class="text-cut cu-tag line-yellow round df">{{ current_item_info.notice }}</text>
						</view> -->

							<view
								v-show="
									current_item_info.asset_band !== undefined &&
										current_item_info.asset_band !== null &&
										current_item_info.asset_band !== ''
								"
								class="text-sm flex"
							>
								<text class="text-grey text-df">
									品牌: {{ current_item_info.asset_band }}
								</text>
							</view>
						</view>
					</view>
				</view>

				<radio-group class="block margin-bottom" @change="RadioChange">
					<view
						class="cu-form-group"
						v-for="(item, index) in item.suppliers"
						:key="index"
					>
						<view class="">
							<view class="title margin-top-xs">{{ item.supplier_name }}</view>
							<view class="flex margin-bottom-xs">
								<text class="text-grey text-df">
									单价: {{ item.supplier_price }}元
								</text>
								<!-- <text class="text-grey text-df">累计: {{ current_item_info.asset_band }}</text> -->
							</view>
						</view>
						<radio
							:class="radio == item.supplier_id ? 'checked' : ''"
							:checked="radio == item.supplier_id ? true : false"
							:value="item.supplier_id"
						></radio>
					</view>
				</radio-group>

				<view class="cu-bar bg-white justify-end">
					<view class="action">
						<button class="cu-btn line-gray text-gray" @tap="hideModal">取消</button>
						<button class="cu-btn bg-gradual-green margin-left" @tap="onAddToCart()">
							加入
						</button>
					</view>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
import { uniFab } from '@dcloudio/uni-ui';
export default {
	components: {
		uniFab
	},
	data() {
		return {
			modalName: null,
			current_item_info: null,
			supplier_id_radio: '',

			showEmpty: false,
			showNoMore: false,

			catList: getApp().globalData.cartList,
			tabCur: 0,
			mainCur: 0,
			verticalNavTop: 0,
			load: true,

			cart_item_id_list: getApp().globalData.cart_item_id_list,
			cartList: [],

			domain: getApp().globalData.domain,
			default_img: 'this.src="' + require('../../static/default.png') + '"',

			directionStr: '垂直',
			horizontal: 'right',
			vertical: 'bottom',
			direction: 'horizontal',
			pattern: {
				color: '#7A7E83',
				backgroundColor: '#fff',
				selectedColor: '#0b988f',
				buttonColor: '#0b988f'
			},
			content: [
				{
					iconPath: '/static/cart.png',
					selectedIconPath: '/static/cart.png',
					text: '物品篮',
					active: true
				}
			],

			cateDetailAllList: []
		};
	},
	onLoad() {
		uni.showLoading({
			title: '加载中...',
			mask: true
		});

		this.cart_item_id_list = getApp().globalData.cart_list_info.map(item => {
			return Object.assign({ id: item.id });
		});

		getApp().globalData.cart_item_id_list = this.cart_item_id_list;
	},
	onShow() {
		this.loadData();
	},
	methods: {
		showModal(e) {
			this.modalName = 'ChooseSupplierModal';
			this.current_item_info = e;
			console.log(e);

			// if (getApp().globalData.cart_list_info.length == 0) {
			// 	getApp().globalData.cart_list_info.push(item);
			// 	this.showToast('成功添加到物品篮');
			// 	console.log(getApp().globalData.cart_list_info);
			// 	return;
			// }

			// for (var i = 0; i < getApp().globalData.cart_list_info.length; i++) {
			// 	if (getApp().globalData.cart_list_info[i].asset_name == item.asset_name) {
			// 		this.showToast(item.asset_name + ' 已添加过了，无须重复添加');
			// 		console.log(getApp().globalData.cart_list_info);
			// 		return;
			// 	}
			// }

			// getApp().globalData.cart_list_info.push(item);
			// console.log(getApp().globalData.cart_list_info);
			// this.showToast(item.asset_name + ' 成功添加到物品篮');
		},
		hideModal(e) {
			this.modalName = null;
		},
		onAdd(item) {
			this.showModal(item);
		},

		onMinus(item) {
			for (var i = 0; i < getApp().globalData.cart_list_info.length; i++) {
				if (getApp().globalData.cart_list_info[i].asset_name == item.asset_name) {
					getApp().globalData.cart_list_info.splice(i, 1);
					this.showToast(item.asset_name + '成功从物品篮删除');
					console.log(getApp().globalData.cart_list_info);
					return;
				}
			}
			this.showToast('物品篮无 ' + item.asset_name + '，无须删除');
			console.log(getApp().globalData.cart_list_info);
		},

		trigger(e) {
			console.log('trigger');
			if (e.index === 0) {
				uni.navigateTo({
					url: '../cart/cart'
				});
			}
		},

		///////////////////////////////////

		successCb(rsp) {
			uni.hideLoading();
			if (rsp.data.error === 0) {
				this.catList = rsp.data.msg.commoditycategory;

				console.log(this.catList);
				getApp().globalData.catList = this.cartList;

				if (this.catList.length > 0) {
					this.showNoMore = true;
				}

				if (this.catList.length == 0) {
					this.showEmpty = true;
					return;
				}

				for (var i = 0; i < this.catList.length; i++) {
					let newArr = this.catList[i].asset_info.map((item, stock, number) => {
						return Object.assign(item, { stock: stock }, { number: 0 });
					});
					newArr.map(item => {
						item.stock = parseInt(item.asset_count);
					});
					this.cartList = newArr;
				}

				this.listCur = this.catList[0];
				this.mainCur = this.catList[0].id;
			}
		},
		failCb(err) {
			uni.hideLoading();
			console.log('api_category failed', err);
		},
		completeCb(rsp) {},

		loadData() {
			this.requestWithMethod(
				getApp().globalData.api_category,
				'GET',
				'',
				this.successCb,
				this.failCb,
				this.completeCb
			);
		},

		TabSelect(e) {
			this.tabCur = e.currentTarget.dataset.id;
			this.mainCur = e.currentTarget.dataset.id;
			this.verticalNavTop = (e.currentTarget.dataset.id - 1) * 50;
		},
		VerticalMain(e) {
			// #ifdef MP-ALIPAY
			return false; //支付宝小程序暂时不支持双向联动
			// #endif
			let that = this;
			let tabHeight = 0;
			if (this.load) {
				for (let i = 0; i < this.catList.length; i++) {
					let view = uni.createSelectorQuery().select('#main-' + this.catList[i].id);
					view.fields(
						{
							size: true
						},
						data => {
							this.catList[i].top = tabHeight;
							tabHeight = tabHeight + data.height;
							this.catList[i].bottom = tabHeight;
						}
					).exec();
				}
				this.load = false;
			}
			let scrollTop = e.detail.scrollTop + 10;
			for (let i = 0; i < this.catList.length; i++) {
				if (scrollTop > this.catList[i].top && scrollTop < this.catList[i].bottom) {
					this.verticalNavTop = (this.catList[i].id - 1) * 50;
					this.tabCur = this.catList[i].id;
					return false;
				}
			}
		}
	}
};
</script>

<style>
.fixed {
	position: fixed;
	z-index: 99;
}

.VerticalNav.nav {
	width: 200upx;
	white-space: initial;
}

.VerticalNav.nav .cu-item {
	width: 100%;
	text-align: center;
	background-color: #fff;
	margin: 0;
	border: none;
	height: 50px;
	position: relative;
}

.VerticalNav.nav .cu-item.cur {
	background-color: #f1f1f1;
}

.VerticalNav.nav .cu-item.cur::after {
	content: '';
	width: 8upx;
	height: 30upx;
	border-radius: 10upx 0 0 10upx;
	position: absolute;
	background-color: currentColor;
	top: 0;
	right: 0upx;
	bottom: 0;
	margin: auto;
}

.VerticalBox {
	display: flex;
}

.VerticalMain {
	background-color: #f1f1f1;
	flex: 1;
}
</style>
