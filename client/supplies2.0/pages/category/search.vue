<template>
	<view>
		<cu-custom bgColor="bg-gradual-blue" :isBack="true">
			<block slot="content">物品搜索</block>
		</cu-custom>

		<view v-show="showEmpty" style="margin-top: 200upx;">
			<view class="flex justify-center align-center margin-left-xl">
				<image src="../../static/empty_icon.png" style="width: 200upx; height: 200upx;" />
			</view>
			<view class="flex justify-center text-gray margin-top">空空如也</view>
		</view>

		<view class="VerticalBox" style="margin-top: 100upx;">
			<scroll-view
				class="VerticalMain"
				scroll-y
				scroll-with-animation
				style="height:calc(100vh - 100upx);"
				:scroll-into-view="'main-' + mainCur"
			>
				<view class="cu-list menu-avatar">
					<view
						class="cu-item"
						style="height: 200upx;"
						v-for="(item2, index2) in assetList"
						:key="index2"
					>
						<view
							class="cu-avatar lg"
							:style="
								item2.asset_image === null
									? 'background-image:url(../../static/default.png);'
									: 'background-image:url(' + domain + item2.asset_image + ');'
							"
						></view>
						<view class="content2" style="width: calc(100% - 70px);">
							<view class="flex">
								<view class="text-grey">{{ item2.asset_name }}</view>
								<!-- <view class="text-grey text-sm margin-left-xs">
								| 库存:{{ item2.asset_count }}
							</view> -->
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
									限价:{{ item2.asset_limit_price }}元
								</text>
							</view>

							<view class="flex justify-between align-center ">
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

								<view class="flex">
									<view
										class="cuIcon-cartfill radius bg-olive  margin-bottom-xs margin-right-sm"
										style="padding-left: 30upx; padding-right: 30upx; padding-top: 8upx; padding-bottom: 8upx;"
										@tap="onAdd(item2)"
									></view>
									<view
										class="cuIcon-deletefill radius bg-orange margin-bottom-xs margin-right-sm"
										style="padding-left: 30upx; padding-right: 30upx; padding-top: 8upx; padding-bottom: 8upx;"
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
								<!-- <view class="text-grey text-df margin-left-xs">
									| 库存:{{ current_item_info.asset_count }}
								</view> -->
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
				<view v-show="showEmptySupplier" class="margin-top">
					<view class="flex justify-center align-center margin-left-xl">
						<image
							src="../../static/empty_icon.png"
							style="width: 100upx; height: 100upx;"
						/>
					</view>
					<view class="flex justify-center text-gray margin-top">暂无供应商选择</view>
				</view>
				<radio-group class="block margin-bottom" @change="RadioChange">
					<view
						class="cu-form-group"
						v-for="(item, index) in item_supplier_list"
						:key="index"
					>
						<view class="">
							<view class="title margin-top-xs">{{ item.supplier_name }}</view>
							<view class="flex margin-bottom-xs">
								<text class="text-grey text-df">
									单价: {{ item.price }}元 / {{ item.asset_unit }}
								</text>
								<!-- <text class="text-grey text-df">累计: {{ current_item_info.asset_band }}</text> -->
							</view>
						</view>
						<radio
							:class="supplier_id_radio == item.id ? 'checked' : ''"
							:checked="supplier_id_radio == item.id ? true : false"
							:value="item.id"
						></radio>
					</view>
				</radio-group>

				<view class="cu-bar bg-white justify-end">
					<view class="action">
						<button class="cu-btn line-gray text-gray" @tap="hideModal">取消</button>
						<button
							:disabled="showEmptySupplier"
							v-show="!is_no_supplier"
							class="cu-btn bg-gradual-green margin-left"
							@tap="onAddToCart()"
						>
							添加
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
			showEmptySupplier: false,
			CustomBar: this.CustomBar,

			modalName: null,
			current_item_info: null,
			supplier_id_radio: -1,

			is_no_supplier: false,

			showEmpty: false,
			showNoMore: false,

			catList: getApp().globalData.cartList,
			tabCur: 0,
			mainCur: 0,
			load: true,

			item_supplier_list: [],

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
				selectedColor: '#2481c4',
				buttonColor: '#59aef9'
			},
			content: [
				{
					iconPath: '/static/cart.png',
					selectedIconPath: '/static/cart.png',
					text: '物品篮',
					active: true
				}
			],

			cateDetailAllList: [],

			assetList: [],

			search_item_name: ''
		};
	},
	onLoad() {
		this.cart_item_id_list = getApp().globalData.cart_list_info.map(item => {
			return Object.assign({ id: item.id });
		});

		getApp().globalData.cart_item_id_list = this.cart_item_id_list;
	},
	onShow() {
		this.loadData();
	},
	methods: {
		RadioChange(e) {
			this.supplier_id_radio = e.detail.value;
			console.log('select supplier: ' + this.supplier_id_radio);

			var supplier = this.getSupplierById(this.supplier_id_radio);

			this.selected_supplier_id = supplier.supplier_name_id;
			this.selected_supplier_name = supplier.supplier_name;
			this.select_supplier_price = supplier.price;
		},

		getSupplierById(supplier_id) {
			if (this.item_supplier_list.length > 0) {
				for (var i = 0; i < this.item_supplier_list.length; i++) {
					let id = this.item_supplier_list[i].id;
					if (id == supplier_id) {
						return this.item_supplier_list[i];
					}
				}
			}
			return '';
		},

		/**
		 * 获取商品供应商列表
		 */
		requestSupplierList(itemSN) {
			this.item_supplier_list = [];

			this.requestWithMethod(
				getApp().globalData.api_get_supplier + itemSN,
				'GET',
				'',
				this.successSupplierCb,
				this.failSupplierCb,
				this.completeSupplierCb
			);
		},
		successSupplierCb(rsp) {
			var isEmpty = true;
			for (var x in rsp.data) {
				isEmpty = false;
			}
			this.showEmptySupplier = isEmpty;

			if (rsp.data.error === 0) {
				this.item_supplier_list = rsp.data.msg.supplier_list;
				console.log('supplier list:');
				console.log(this.item_supplier_list);
			}
		},
		failSupplierCb(err) {
			console.log('api_get_supplier failed', err);
		},
		completeSupplierCb(rsp) {},

		////////////

		showModal(e) {
			this.modalName = 'ChooseSupplierModal';
			this.current_item_info = e;
			console.log(e);
			this.requestSupplierList(this.current_item_info.asset_sn);
		},
		hideModal(e) {
			this.modalName = null;
		},
		onAdd(item) {
			this.showModal(item);
		},

		onAddToCart() {
			console.log('supplier: ' + this.selected_supplier_name);
			this.current_item_info.selected_supplier_name = this.selected_supplier_name;
			this.current_item_info.selected_supplier = this.selected_supplier_id;
			this.current_item_info.selected_supplier_price = this.select_supplier_price;

			let isExceed = false;
			let item_limit_price = parseFloat(this.current_item_info.asset_limit_price);
			let supplier_price = parseFloat(this.select_supplier_price);

			if (item_limit_price == 0.0) {
				isExceed = false;
			} else if (item_limit_price < supplier_price) {
				isExceed = true;
			}

			this.current_item_info.is_exceed = isExceed;

			if (getApp().globalData.cart_list_info.length == 0) {
				getApp().globalData.cart_list_info.push(this.current_item_info);
				this.showToast('成功添加到物品篮');
				console.log(getApp().globalData.cart_list_info);
				this.hideModal();
				return;
			}

			for (var i = 0; i < getApp().globalData.cart_list_info.length; i++) {
				if (
					getApp().globalData.cart_list_info[i].asset_sn ==
					this.current_item_info.asset_sn
				) {
					this.showToast(this.current_item_info.asset_sn + ' 已添加过了，无须重复添加');
					console.log(getApp().globalData.cart_list_info);
					this.hideModal();
					return;
				}
			}

			getApp().globalData.cart_list_info.push(this.current_item_info);
			console.log(getApp().globalData.cart_list_info);
			this.showToast(this.current_item_info.asset_name + ' 成功添加到物品篮');
			this.hideModal();
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
			if (rsp.data.error === 0) {
				this.assetList = rsp.data.msg.asset_info;
				console.log('asset_info:');
				console.log(this.assetList);

				if (this.assetList.length > 0) {
					this.showNoMore = true;
				}

				if (this.assetList.length == 0) {
					this.showEmpty = true;
					return;
				}

				// for (var i = 0; i < this.assetList.length; i++) {
				// 	let newArr = this.assetList.map((item, stock, number) => {
				// 		return Object.assign(item, { stock: stock }, { number: 0 },{selected_supplier:-1},{selected_supplier_name:''});
				// 	});
				// 	newArr.map(item => {
				// 		item.stock = parseInt(item.asset_count);
				// 	});
				// 	this.assetList = newArr;
				// }

				let newArr = this.assetList.map((item, stock, number) => {
					return Object.assign(
						item,
						{ stock: 999 },
						{ number: 0 },
						{ total_price: 0 },
						{ selected_supplier: 0 },
						{ selected_supplier_name: '' },
						{ selected_supplier_price: '' },
						{ is_exceed: false }
					);
				});
				newArr.map(item => {
					item.stock = parseInt(item.asset_count);
				});
				this.assetList = newArr;
				console.log(this.assetList);
			}
			uni.hideLoading();
		},
		failCb(err) {
			uni.hideLoading();
			console.log('api_category failed', err);
		},
		completeCb(rsp) {},

		loadData() {
			uni.showLoading({
				title: '搜索中...',
				mask: true
			});
			this.requestWithMethod(
				getApp().globalData.get_asset_by_cname + getApp().globalData.search_item_name,
				'GET',
				'',
				this.successCb,
				this.failCb,
				this.completeCb
			);
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
